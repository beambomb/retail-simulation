from dataclasses import dataclass
from .enums import ShiftType


@dataclass
class ShiftLog:
    shift_id: str
    cashier_id: str
    counter_id: int
    date: str
    shift_type: ShiftType
    transactions_processed: int
    errors_occurred: int
    peak_fatigue: float
