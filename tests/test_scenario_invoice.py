import unittest
from decimal import Decimal

from proteus import Model
from trytond.modules.account.tests.tools import (create_chart, create_tax,
                                                 get_accounts)
from trytond.modules.company.tests.tools import create_company, get_company
from trytond.tests.test_tryton import drop_db
from trytond.tests.tools import activate_modules


class Test(unittest.TestCase):

    def setUp(self):
        drop_db()
        super().setUp()

    def tearDown(self):
        drop_db()
        super().tearDown()

    def test(self):

        # Install account_invoice_price_list module
        activate_modules('account_invoice_price_list')

        # Create company
        _ = create_company()
        company = get_company()

        # Create chart of accounts
        _ = create_chart(company)
        accounts = get_accounts(company)
        revenue = accounts['revenue']
        expense = accounts['expense']

        # Create tax
        tax = create_tax(Decimal('.10'))
        tax.save()

        # Create party
        Party = Model.get('party.party')
        party = Party(name='Party')
        party.save()

        # Create account category
        ProductCategory = Model.get('product.category')
        account_category = ProductCategory(name="Account Category")
        account_category.accounting = True
        account_category.account_expense = expense
        account_category.account_revenue = revenue
        account_category.customer_taxes.append(tax)
        account_category.save()

        # Create product
        ProductUom = Model.get('product.uom')
        unit, = ProductUom.find([('name', '=', 'Unit')])
        ProductTemplate = Model.get('product.template')
        template = ProductTemplate()
        template.name = 'product'
        template.default_uom = unit
        template.type = 'service'
        template.list_price = Decimal('20.00')
        template.account_category = account_category
        template.save()
        product, = template.products

        # Create Customer invoice
        Invoice = Model.get('account.invoice')
        InvoiceLine = Model.get('account.invoice.line')
        customer_invoice = Invoice()
        customer_invoice.party = party
        customer_invoice.type = 'out'

        # Create Supplier invoice
        supplier_invoice = Invoice()
        supplier_invoice.party = party
        supplier_invoice.type = 'in'

        # Customer: Add line defining product (Unit Price is calculated)
        customer_line = InvoiceLine()
        customer_invoice.lines.append(customer_line)
        customer_line.product = product
        customer_line.quantity = 3
        self.assertEqual(customer_line.unit_price, Decimal('20.00'))
        self.assertEqual(customer_line.amount, Decimal('60.00'))

        # Supplier: Add line defining product (Unit Price is calculated)
        supplier_line = InvoiceLine()
        supplier_invoice.lines.append(supplier_line)
        supplier_line.product = product
        supplier_line.quantity = 2
        self.assertEqual(supplier_line.unit_price, Decimal('20.00'))
        self.assertEqual(supplier_line.amount, Decimal('40.00'))
