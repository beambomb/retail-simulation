import random
from typing import List, Tuple
from ..domain import Customer, Product
from ..catalog import CatalogRepository
from .customer_base import CustomerShoppingStrategy


class FamilyStockerStrategy(CustomerShoppingStrategy):
    def select_items(self, customer: Customer, catalog: CatalogRepository) -> List[Tuple[Product, int]]:
        products = catalog.get_all()
        groceries = [p for p in products if p.category in ("Groceries", "Household", "Personal Care")]
        item_count = random.randint(8, 18)
        selected_base = random.sample(groceries, min(item_count, len(groceries)))
        basket: List[Tuple[Product, int]] = []
        for p in selected_base:
            qty = random.choices([1, 2, 3, 5], weights=[0.4, 0.35, 0.15, 0.1])[0]
            basket.append((p, qty))
            affinities = catalog.get_affinities(p.sku)
            if affinities and random.random() < 0.65:
                aff_sku = random.choice(affinities)
                aff_prod = catalog.get_by_sku(aff_sku)
                if not any(item[0].sku == aff_sku for item in basket):
                    basket.append((aff_prod, random.choice([1, 2])))
        return basket
