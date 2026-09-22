import random
from typing import List
from .models import (
    Customer,
    Cashier,
    PersonaType,
    ExperienceLevel,
    ShiftType,
    SimulationConfig,
)


class CustomerFactory:
    @staticmethod
    def create_customer(customer_idx: int, config: SimulationConfig) -> Customer:
        personas = [
            PersonaType.QUICK_GRAB,
            PersonaType.FAMILY_STOCKER,
            PersonaType.BUDGET_HUNTER,
            PersonaType.IMPULSE_BUYER,
        ]
        weights = [
            config.quick_grab_ratio,
            config.family_stocker_ratio,
            config.budget_hunter_ratio,
            config.impulse_buyer_ratio,
        ]
        chosen_persona = random.choices(personas, weights=weights)[0]

        if chosen_persona == PersonaType.QUICK_GRAB:
            budget = float(random.randint(15000, 60000))
            patience = random.randint(3, 5)
            has_loyalty = random.random() < 0.20
        elif chosen_persona == PersonaType.FAMILY_STOCKER:
            budget = float(random.randint(250000, 900000))
            patience = random.randint(8, 15)
            has_loyalty = random.random() < 0.85
        elif chosen_persona == PersonaType.BUDGET_HUNTER:
            budget = float(random.randint(75000, 180000))
            patience = random.randint(5, 8)
            has_loyalty = random.random() < 0.45
        else:
            budget = float(random.randint(50000, 200000))
            patience = random.randint(4, 7)
            has_loyalty = random.random() < 0.35

        customer_id = f"CUST-{customer_idx:05d}"
        phone = f"0812{random.randint(10000000, 99999999)}" if has_loyalty else None

        return Customer(
            customer_id=customer_id,
            persona=chosen_persona,
            budget=budget,
            patience_threshold=patience,
            has_loyalty=has_loyalty,
            phone_number=phone,
        )


class CashierFactory:
    _CASHIER_NAMES = [
        "Ahmad Fauzi",
        "Siti Rahmawati",
        "Budi Santoso",
        "Dewi Lestari",
        "Rizky Pratama",
        "Nurul Hidayah",
        "Eko Prasetyo",
        "Putri Wulandari",
    ]

    @classmethod
    def create_cashiers(cls, count: int, junior_ratio: float) -> List[Cashier]:
        cashiers: List[Cashier] = []
        for i in range(count):
            name = cls._CASHIER_NAMES[i % len(cls._CASHIER_NAMES)]
            is_junior = random.random() < junior_ratio
            experience = ExperienceLevel.JUNIOR if is_junior else ExperienceLevel.SENIOR
            shift = ShiftType.MORNING if i % 2 == 0 else ShiftType.EVENING
            base_error = 0.035 if is_junior else 0.015
            speed = 2.2 if is_junior else 1.2
            cashiers.append(
                Cashier(
                    cashier_id=f"CSH-{i + 1:03d}",
                    name=name,
                    experience=experience,
                    shift=shift,
                    counter_id=(i % 4) + 1,
                    base_error_rate=base_error,
                    scan_speed_sec=speed,
                    fatigue=0.0,
                )
            )
        return cashiers
