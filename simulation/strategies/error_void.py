import random
from typing import List
from ..domain import Cashier, Customer, TransactionItem, PersonaType, ErrorCategory
from ..catalog import CatalogRepository
from .error_base import CashierErrorStrategy


class VoidStrategy(CashierErrorStrategy):
    def apply_error(
        self,
        cashier: Cashier,
        customer: Customer,
        item: TransactionItem,
        catalog: CatalogRepository,
        multiplier: float,
    ) -> List[TransactionItem]:
        prob = 0.01 * multiplier
        if customer.persona == PersonaType.BUDGET_HUNTER:
            prob = 0.045 * multiplier
        if random.random() < prob:
            item.is_void = True
            item.error_type = ErrorCategory.VOID_ITEM
        return [item]
