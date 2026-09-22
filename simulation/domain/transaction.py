from dataclasses import dataclass, field
from typing import List
from .enums import PaymentMethod, ErrorCategory


@dataclass
class TransactionItem:
    item_id: str
    transaction_id: str
    sequence: int
    sku: str
    product_name: str
    quantity: int
    unit_price: float
    subtotal: float
    discount_applied: float = 0.0
    is_void: bool = False
    error_type: ErrorCategory = ErrorCategory.NONE


@dataclass
class Transaction:
    transaction_id: str
    store_id: str
    cashier_id: str
    customer_id: str
    timestamp: str
    payment_method: PaymentMethod
    total_amount: float
    item_count: int
    has_error: bool = False
    items: List[TransactionItem] = field(default_factory=list)
