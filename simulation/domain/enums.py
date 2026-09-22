from enum import Enum


class PersonaType(str, Enum):
    QUICK_GRAB = "QUICK_GRAB"
    FAMILY_STOCKER = "FAMILY_STOCKER"
    BUDGET_HUNTER = "BUDGET_HUNTER"
    IMPULSE_BUYER = "IMPULSE_BUYER"


class PaymentMethod(str, Enum):
    CASH = "CASH"
    DEBIT = "DEBIT"
    QRIS = "QRIS"
    CREDIT = "CREDIT"


class ExperienceLevel(str, Enum):
    JUNIOR = "JUNIOR"
    SENIOR = "SENIOR"


class ShiftType(str, Enum):
    MORNING = "MORNING"
    EVENING = "EVENING"


class ErrorCategory(str, Enum):
    NONE = "NONE"
    DOUBLE_SCAN = "DOUBLE_SCAN"
    TYPO_SKU = "TYPO_SKU"
    VOID_ITEM = "VOID_ITEM"
    MISSING_MEMBER = "MISSING_MEMBER"
    WRONG_PAYMENT = "WRONG_PAYMENT"
