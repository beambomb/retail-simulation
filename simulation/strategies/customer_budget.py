import random
from typing import List, Tuple
from ..domain import Customer, Product
from ..catalog import CatalogRepository
from .customer_base import CustomerShoppingStrategy


class BudgetHunterStrategy(CustomerShoppingStrategy):
    def select_items(self, customer: Customer, catalog: CatalogRepository) -> List[Tuple[Product, int]]:
        products = catalog.get_all()
        affordable = sorted(products, key=lambda x: x.sell_price)
        candidate_count = random.randint(4, 9)
        candidates = affordable[:20]
        selected = random.sample(candidates, min(candidate_count, len(candidates)))
        basket: List[Tuple[Product, int]] = []
        running_total = 0.0
        for p in selected:
            qty = random.choice([1, 2])
            cost = p.sell_price * qty
            if running_total + cost <= customer.budget * 1.15:
                basket.append((p, qty))
                running_total += cost
        if not basket and products:
            basket.append((affordable[0], 1))
        return basket
