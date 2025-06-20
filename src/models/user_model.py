from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Numeric
from src.database.database import Base

class User(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True, index=True)
    sector = Column(String, nullable=False)
    active = Column(Boolean, default=True)
    role = Column(String, nullable=False)
