# This file is part of the account_invoice_price_list module for Tryton.
# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
import unittest
import trytond.tests.test_tryton
from trytond.tests.test_tryton import ModuleTestCase


class AccountInvoicePriceListTestCase(ModuleTestCase):
    'Test Account Invoice Price List module'
    module = 'account_invoice_price_list'


def suite():
    suite = trytond.tests.test_tryton.suite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(
        AccountInvoicePriceListTestCase))
    return suite