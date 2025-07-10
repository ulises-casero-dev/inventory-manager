from enum import Enum

class MovementType(str, Enum):
    PURCHASE = "purchase"
    SALE = "sale"
    ADJUSTAMENT = "adjustament"
    RETURN_FROM_CUSTOMER = "return_from_customer"
    INVENTORY_CORRECTION = "inventory_correction"
    TRANSFER = "transfer"
    INITIAL = "initial"