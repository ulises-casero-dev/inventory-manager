from src.database.database import Base, engine
from src.models import (
    product_model,
    category_model,
    stock_model,
    user_model,
    order_model,
    order_item_model
)

if __name__ == '__main__':
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully")

    