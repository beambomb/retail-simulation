import random
from typing import List
from ..domain import Cashier, Customer, Transaction, TransactionItem, PaymentMethod, ErrorCategory
from ..catalog import CatalogRepository
from .error_double_scan import DoubleScanStrategy
from .error_typo import ManualTypoStrategy
from .error_void import VoidStrategy


class CashierErrorEngine:
    def __init__(self):
        self._double_scan = DoubleScanStrategy()
        self._manual_typo = ManualTypoStrategy()
        self._void_handler = VoidStrategy()

    def process_item(
        self,
        cashier: Cashier,
        customer: Customer,
        item: TransactionItem,
        catalog: CatalogRepository,
        multiplier: float,
    ) -> List[TransactionItem]:
        items = self._manual_typo.apply_error(cashier, customer, item, catalog, multiplier)
        final_items: List[TransactionItem] = []
        for it in items:
            scan_results = self._double_scan.apply_error(cashier, customer, it, catalog, multiplier)
            for s_it in scan_results:
                void_results = self._void_handler.apply_error(cashier, customer, s_it, catalog, multiplier)
                final_items.extend(void_results)
        return final_items

    def resolve_payment_and_loyalty(
        self, cashier: Cashier, customer: Customer, transaction: Transaction, multiplier: float
    ) -> None:
        fatigue_factor = 1.0 + (cashier.fatigue * 1.5)
        if customer.has_loyalty:
            miss_prob = 0.05 * fatigue_factor * multiplier
            if random.random() < miss_prob:
                customer.has_loyalty = False
                transaction.customer_id = "CUST-GUEST"
                transaction.has_error = True
        wrong_pay_prob = 0.02 * fatigue_factor * multiplier
        if random.random() < wrong_pay_prob:
            alternative_methods = [m for m in PaymentMethod if m != transaction.payment_method]
            transaction.payment_method = random.choice(alternative_methods)
            transaction.has_error = True
