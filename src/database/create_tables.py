from src.database.database import Base, engine
from src.models import (
    category_model,
    product_model,
    product_suppliers,
    purchase_item_model,
    purchase_model,
    stock_model,
    stock_movement_model,
    supplier_model,
    user_model
)

if __name__ == '__main__':
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully")

    