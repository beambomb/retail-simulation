from ..domain import PersonaType
from .customer_base import CustomerShoppingStrategy
from .customer_quick_grab import QuickGrabStrategy
from .customer_family import FamilyStockerStrategy
from .customer_budget import BudgetHunterStrategy
from .customer_impulse import ImpulseBuyerStrategy


class StrategyFactory:
    _strategies = {
        PersonaType.QUICK_GRAB: QuickGrabStrategy(),
        PersonaType.FAMILY_STOCKER: FamilyStockerStrategy(),
        PersonaType.BUDGET_HUNTER: BudgetHunterStrategy(),
        PersonaType.IMPULSE_BUYER: ImpulseBuyerStrategy(),
    }

    @classmethod
    def get_shopping_strategy(cls, persona: PersonaType) -> CustomerShoppingStrategy:
        return cls._strategies.get(persona, QuickGrabStrategy())
