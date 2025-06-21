from sqlalchemy.orm import Session
from src.models.stock_model import Stock
from src.schemas.stock_schema import StockCreate, StockUpdate

def get_all_stocks(db: Session):
    return db.query(Stock).all()

def create_stock(db: Session, stock_data: StockCreate):
    new_stock = Stock(**stock_data.dict())
    db.add(new_stock)
    db.commit()
    db.refresh(new_stock)
    return new_stock

def get_stok_by_id(db: Session, id: int):
    return db.get(Stock, id)

def update_stock(db: Session, id: int, stock_data: StockUpdate):
    stock = db.get(Stock, id)
    if not stock:
        return None
    
    stock.quantity = stock_data.quantity
    db.commit()
    db.refresh(stock)
    return stock

