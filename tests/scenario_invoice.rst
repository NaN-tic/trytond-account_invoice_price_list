================
Invoice Scenario
================

Imports::

    >>> import datetime
    >>> from dateutil.relativedelta import relativedelta
    >>> from decimal import Decimal
    >>> from operator import attrgetter
    >>> from proteus import Model, Wizard
    >>> from trytond.tests.tools import activate_modules
    >>> from trytond.modules.product import price_digits
    >>> from trytond.modules.company.tests.tools import create_company, \
    ...     get_company
    >>> from trytond.modules.account.tests.tools import create_fiscalyear, \
    ...     create_chart, get_accounts, create_tax
    >>> from trytond.modules.account_invoice.tests.tools import \
    ...     set_fiscalyear_invoice_sequences, create_payment_term
    >>> today = datetime.date.today()

Install account_invoice_price_list module::

    >>> config = activate_modules('account_invoice_price_list')

Create company::

    >>> _ = create_company()
    >>> company = get_company()

Create chart of accounts::

    >>> _ = create_chart(company)
    >>> accounts = get_accounts(company)
    >>> receivable = accounts['receivable']
    >>> revenue = accounts['revenue']
    >>> expense = accounts['expense']
    >>> account_tax = accounts['tax']

Create tax::

    >>> tax = create_tax(Decimal('.10'))
    >>> tax.save()

Create party::

    >>> Party = Model.get('party.party')
    >>> party = Party(name='Party')
    >>> party.save()

Create account category::

    >>> ProductCategory = Model.get('product.category')
    >>> account_category = ProductCategory(name="Account Category")
    >>> account_category.accounting = True
    >>> account_category.account_expense = expense
    >>> account_category.account_revenue = revenue
    >>> account_category.customer_taxes.append(tax)
    >>> account_category.save()

Create product::

    >>> ProductUom = Model.get('product.uom')
    >>> unit, = ProductUom.find([('name', '=', 'Unit')])
    >>> ProductTemplate = Model.get('product.template')
    >>> template = ProductTemplate()
    >>> template.name = 'product'
    >>> template.default_uom = unit
    >>> template.type = 'service'
    >>> template.list_price = Decimal('20.00')
    >>> template.account_category = account_category
    >>> template.save()
    >>> product, = template.products
    >>> product.cost_price = Decimal('30.00')
    >>> product.save()

Create Customer invoice::

    >>> Invoice = Model.get('account.invoice')
    >>> InvoiceLine = Model.get('account.invoice.line')
    >>> customer_invoice = Invoice()
    >>> customer_invoice.party = party
    >>> customer_invoice.type = 'out'

Create Supplier invoice::

    >>> supplier_invoice = Invoice()
    >>> supplier_invoice.party = party
    >>> supplier_invoice.type = 'in'

Customer: Add line defining product (Unit Price is calculated)::

    >>> customer_line = InvoiceLine()
    >>> customer_invoice.lines.append(customer_line)
    >>> customer_line.product = product
    >>> customer_line.quantity = 3
    >>> customer_line.unit_price == Decimal('20.00')
    True
    >>> customer_line.amount == Decimal('60.00')
    True

Supplier: Add line defining product (Unit Price is calculated)::

    >>> supplier_line = InvoiceLine()
    >>> supplier_invoice.lines.append(supplier_line)
    >>> supplier_line.product = product
    >>> supplier_line.quantity = 2
    >>> supplier_line.unit_price == Decimal('30.00')
    True
    >>> supplier_line.amount == Decimal('60.00')
    True
