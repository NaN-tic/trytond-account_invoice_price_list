#This file is part account_invoice_price_list module for Tryton.
#The COPYRIGHT file at the top level of this repository contains
#the full copyright notices and license terms.
from trytond.pool import Pool, PoolMeta
from trytond.transaction import Transaction

__all__ = ['InvoiceLine']
__metaclass__ = PoolMeta

class InvoiceLine:
    'Invoice Line'
    __name__ = 'account.invoice.line'

    def on_change_product(self):
        Product = Pool().get('product.product')
        res = super(InvoiceLine, self).on_change_product()
        if self.invoice.party and self.invoice.party.sale_price_list and \
                self.invoice.type in ['out_invoice', 'out_credit_note'] and \
                self.product:
            with Transaction().set_context({
                    'price_list': self.invoice.party.sale_price_list.id,
                    'customer': self.invoice.party.id,
                }):
                res['unit_price'] = Product.get_sale_price([self.product],
                self.quantity or 0)[self.product.id]
        return res
