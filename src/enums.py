from enum import Enum

class UserRole(str, Enum):
    ADMIN = "admin"
    MANAGE = "manager"
    EMPLOYEE = "employee"

class OrderStatus(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    IN_PROGRESS = "in_progress"
    FULFILLED = "fulfilled"
    DISPACHED = "dispatched"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"
    FAILED = "failed"

class Sector(str, Enum):
    SALES = "sales"
    LOGISTICS = "logistics"
    TRANSPORT = "transport"

class MovementType(str, Enum):
    PURCHASE = "purchase"
    SALE = "sale"
    ADJUSTAMENT = "adjustament"
    RETURN_FROM_CUSTOMER = "return_from_customer"
    INVENTORY_CORRECTION = "inventory_correction"
    TRANSFER = "transfer"
    INITIAL = "initial"
