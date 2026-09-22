import random
from typing import List, Tuple
from ..domain import Customer, Product
from ..catalog import CatalogRepository
from .customer_base import CustomerShoppingStrategy


class ImpulseBuyerStrategy(CustomerShoppingStrategy):
    def select_items(self, customer: Customer, catalog: CatalogRepository) -> List[Tuple[Product, int]]:
        products = catalog.get_all()
        base_items = random.sample(products, random.randint(2, 5))
        basket: List[Tuple[Product, int]] = [(p, 1) for p in base_items]
        impulse_pool = [p for p in products if p.category == "Snacks & Drinks" and p.sell_price <= 20000.0]
        if impulse_pool:
            impulse_count = random.randint(1, 3)
            impulse_items = random.sample(impulse_pool, min(impulse_count, len(impulse_pool)))
            for imp in impulse_items:
                basket.append((imp, random.choice([1, 2])))
        return basket
