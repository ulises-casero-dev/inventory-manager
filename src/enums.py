from enum import Enum

class UserRole(str, Enum):
    admin = "admin"
    manage = "manager"
    employee = "employee"

class OrderStatus(str, Enum):
    pending = "pending"
    approved = "approved"
    in_progress = "in_progress"
    fulfilled = "fulfilled"
    dispatched = "dispatched"
    delivered = "delivered"
    cancelled = "cancelled"
    failed = "failed"

class Sector(str, Enum):
    sales = "sales"
    logistics = "logistics"
    transport = "transport"
