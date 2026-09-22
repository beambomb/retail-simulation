from dataclasses import dataclass
from .enums import ExperienceLevel, ShiftType


@dataclass
class Cashier:
    cashier_id: str
    name: str
    experience: ExperienceLevel
    shift: ShiftType
    counter_id: int
    base_error_rate: float
    scan_speed_sec: float
    fatigue: float = 0.0
