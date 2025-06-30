from typing import List
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import func
from src.models.stock_movement import StockMovement
from src.models.product_model import Product
from src.schemas.stock_movement_schema import StockMovementCreate, StockMovementUpdate

def get_all_movements(db: Session):
    return db.query(StockMovement).all()

def get_movement_by_id(db: Session, id: int):
    return db.get(StockMovement, id)

def create_movement(db: Session, movement_data: StockMovementCreate):
    try:
        new_movement = StockMovement(**movement_data.model_dump())
        db.add(new_movement)
        db.commit()
        db.refresh(new_movement)
        return new_movement

    except SQLAlchemyError as e:
        db.rollback()
        print(f'Database error: {e}')
        return None
    
def update_movement(db: Session, id: int, stock_movement_data: StockMovementUpdate):
    try:
        stock_movement = db.get(StockMovement, id)

        if not stock_movement:
            return None

        update_data = stock_movement_data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(stock_movement, key, value)
        
        db.commit()
        db.refresh(stock_movement)
        return stock_movement
    
    except SQLAlchemyError as e:
        db.rollback()
        print(f'Database error: {e}')
        return None

def cancel_stock_movement(db: Session, id: int):
    try:
        stock_movement = db.get(StockMovement, id)

        if not stock_movement:
            return None

        stock_movement.canceled = True
    
        db.commit()
        db.refresh(stock_movement)
        return stock_movement
    
    except SQLAlchemyError as e:
        db.rollback()
        print(f'Database error: {e}')
        return None