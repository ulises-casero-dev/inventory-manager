from enum import Enum

class UserRole(str, Enum):
    ADMIN = "admin"
    MANAGE = "manager"
    EMPLOYEE = "employee"