import random
from typing import List
from ..domain import Cashier, Customer, TransactionItem, ExperienceLevel, ErrorCategory
from ..catalog import CatalogRepository
from .error_base import CashierErrorStrategy


class ManualTypoStrategy(CashierErrorStrategy):
    def apply_error(
        self,
        cashier: Cashier,
        customer: Customer,
        item: TransactionItem,
        catalog: CatalogRepository,
        multiplier: float,
    ) -> List[TransactionItem]:
        base_product = catalog.get_by_sku(item.sku)
        fatigue_factor = 1.0 + (cashier.fatigue * 2.0)
        experience_factor = 1.8 if cashier.experience == ExperienceLevel.JUNIOR else 0.6
        prob = (base_product.damaged_barcode_prob * 0.4) * fatigue_factor * experience_factor * multiplier
        if random.random() < prob:
            sku_digits = list(item.sku)
            if len(sku_digits) >= 6:
                idx = random.randint(4, len(sku_digits) - 1)
                sku_digits[idx] = str((int(sku_digits[idx]) + random.choice([1, 2, -1])) % 10)
                mutated_sku = "".join(sku_digits)
                replacement = catalog.get_by_sku(mutated_sku)
                item.sku = mutated_sku
                item.product_name = replacement.name
                item.unit_price = replacement.sell_price if replacement.sell_price > 0 else item.unit_price
                item.subtotal = item.unit_price * item.quantity
                item.error_type = ErrorCategory.TYPO_SKU
        return [item]
