from abc import ABC, abstractmethod
from typing import List
from ..domain import Cashier, Customer, TransactionItem
from ..catalog import CatalogRepository


class CashierErrorStrategy(ABC):
    @abstractmethod
    def apply_error(
        self,
        cashier: Cashier,
        customer: Customer,
        item: TransactionItem,
        catalog: CatalogRepository,
        multiplier: float,
    ) -> List[TransactionItem]:
        pass
