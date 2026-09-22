import random
from typing import List, Tuple
from ..domain import Customer, Product
from ..catalog import CatalogRepository
from .customer_base import CustomerShoppingStrategy


class QuickGrabStrategy(CustomerShoppingStrategy):
    def select_items(self, customer: Customer, catalog: CatalogRepository) -> List[Tuple[Product, int]]:
        products = catalog.get_all()
        snacks_drinks = [p for p in products if p.category in ("Snacks & Drinks", "Fresh & Dairy")]
        item_count = random.randint(1, 3)
        selected = random.sample(snacks_drinks, min(item_count, len(snacks_drinks)))
        return [(p, 1) for p in selected]
