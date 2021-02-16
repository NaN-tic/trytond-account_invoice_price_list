#This file is part account_invoice_price_list module for Tryton.
#The COPYRIGHT file at the top level of this repository contains
#the full copyright notices and license terms.
from trytond.pool import Pool, PoolMeta
from trytond.model import fields
from trytond.transaction import Transaction

__all__ = ['InvoiceLine']


class InvoiceLine(metaclass=PoolMeta):
    __name__ = 'account.invoice.line'

    @fields.depends(methods=['get_price_list'])
    def on_change_product(self):
        self.get_price_list()
        super(InvoiceLine, self).on_change_product()

    @fields.depends(methods=['get_price_list'])
    def on_change_quantity(self):
        self.get_price_list()
        try:
            super(InvoiceLine, self).on_change_quantity()
        except:
            pass

    @fields.depends('product', 'party', 'invoice', 'quantity', 'invoice_type',
        '_parent_invoice.type', '_parent_invoice.party', 'unit_price')
    def get_price_list(self):
        pool = Pool()
        Product = pool.get('product.product')

        party = self.party or self.invoice and self.invoice.party
        if not party:
            super(InvoiceLine, self).on_change_product()

        invoice_type = self.invoice.type if self.invoice else self.invoice_type
        if (party and party.sale_price_list and self.product
                and invoice_type == 'out'):
            with Transaction().set_context({
                    'price_list': party.sale_price_list.id,
                    'customer': party.id,
                    }):
                prices = Product.get_sale_price([self.product], self.quantity or
                    0)
                self.unit_price = prices[self.product.id]
        elif (party and self.product and invoice_type == 'in' and hasattr(
                    self.product, 'product_suppliers')):
            with Transaction().set_context({
                    'supplier': party.id,
                    }):
                prices = Product.get_purchase_price([self.product],
                    self.quantity or 0)
                self.unit_price = prices[self.product.id]
        elif self.product:
            self.unit_price = self.product.list_price
        else:
            self.unit_price = None
