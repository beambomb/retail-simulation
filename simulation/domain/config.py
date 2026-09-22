from dataclasses import dataclass


@dataclass
class SimulationConfig:
    days: int = 7
    customers_per_day: int = 120
    cashier_count: int = 4
    error_multiplier: float = 1.0
    fatigue_sensitivity: float = 1.0
    enable_seasonality: bool = True
    junior_cashier_ratio: float = 0.5
    quick_grab_ratio: float = 0.35
    family_stocker_ratio: float = 0.25
    budget_hunter_ratio: float = 0.25
    impulse_buyer_ratio: float = 0.15
