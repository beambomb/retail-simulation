import random
from typing import List
from ..domain import Cashier, Customer, TransactionItem, ExperienceLevel, ErrorCategory
from ..catalog import CatalogRepository
from .error_base import CashierErrorStrategy


class DoubleScanStrategy(CashierErrorStrategy):
    def apply_error(
        self,
        cashier: Cashier,
        customer: Customer,
        item: TransactionItem,
        catalog: CatalogRepository,
        multiplier: float,
    ) -> List[TransactionItem]:
        fatigue_factor = 1.0 + (cashier.fatigue * 1.5)
        experience_factor = 1.4 if cashier.experience == ExperienceLevel.SENIOR else 0.8
        prob = 0.015 * cashier.base_error_rate * fatigue_factor * experience_factor * multiplier
        if random.random() < prob:
            dup_item = TransactionItem(
                item_id=f"{item.item_id}_DUP",
                transaction_id=item.transaction_id,
                sequence=item.sequence + 1,
                sku=item.sku,
                product_name=item.product_name,
                quantity=1,
                unit_price=item.unit_price,
                subtotal=item.unit_price,
                discount_applied=0.0,
                is_void=False,
                error_type=ErrorCategory.DOUBLE_SCAN,
            )
            return [item, dup_item]
        return [item]
