from enum import Enum

class Sector(str, Enum):
    SALES = "sales"
    LOGISTICS = "logistics"
    TRANSPORT = "transport"