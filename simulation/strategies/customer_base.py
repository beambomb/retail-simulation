from abc import ABC, abstractmethod
from typing import List, Tuple
from ..domain import Customer, Product
from ..catalog import CatalogRepository


class CustomerShoppingStrategy(ABC):
    @abstractmethod
    def select_items(self, customer: Customer, catalog: CatalogRepository) -> List[Tuple[Product, int]]:
        pass
