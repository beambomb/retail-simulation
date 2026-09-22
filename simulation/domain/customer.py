from dataclasses import dataclass
from typing import Optional
from .enums import PersonaType


@dataclass
class Customer:
    customer_id: str
    persona: PersonaType
    budget: float
    patience_threshold: int
    has_loyalty: bool
    phone_number: Optional[str] = None
