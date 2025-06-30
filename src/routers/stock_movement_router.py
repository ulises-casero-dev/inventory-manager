from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from src.schemas.stock_movement_schema import StockMovementCreate, StockMovementUpdate, StockMovementResponse
from src.database.database import get_db
from src.services.stock_movement_service import (
    get_all_movements as get_all_movements_service,
    get_movement_by_id as get_movement_by_id_service,
    create_movement as create_movement_service,
    update_movement as update_movement_service,
    cancel_stock_movement as cancel_stock_movement_service 
)

stock_movement_router = APIRouter(
    prefix="/stock_movements",
    tags=["Stock Movements"]
)

@stock_movement_router.get('/stock_movements', status_code=200, response_model=List[StockMovementResponse], response_description='List of stock movements')
def get_stock_movements(db: Session = Depends(get_db)):
    stock_movements = get_all_movements_service(db)
    if not stock_movements:
        raise HTTPException(status_code=404, detail='Srock movements not found')
    return stock_movements

@stock_movement_router.get('/stock_movements/{id}', status_code=200, response_model=StockMovementResponse, response_description='Returns a stock movement if exists')
def get_stock_movement_by_id(id: int, db: Session = Depends(get_db)):
    stock_movement = get_movement_by_id_service(db, id)
    if not stock_movement:
        raise HTTPException(status_code=404, detail='Stock movement not found')
    return stock_movement

@stock_movement_router.post('/stock_movements', status_code=201, response_model=StockMovementResponse, response_description='Creates a new stock movement record')
def create_stock_movement(create_data: StockMovementCreate, db: Session = Depends(get_db)):
    new_stock_movement = create_movement_service(db, create_data)
    if not new_stock_movement:
        raise HTTPException(status_code=400, detail='Stock movement record could not be created')
    return new_stock_movement

@stock_movement_router.put('/stock_movements/{id}', status_code=200, response_model=StockMovementResponse, response_description='Updates an stock movement record')
def update_stock_movement(id:int, update_data: StockMovementUpdate, db: Session = Depends(get_db)):
    updated_stock_movement = update_movement_service(db, id, update_data)
    if not updated_stock_movement:
        raise HTTPException(status_code=400, detail='Stock movement record could not be updated')
    return updated_stock_movement

@stock_movement_router.delete('/stock_movements/{id}', status_code=200, response_model=StockMovementResponse, response_description='Cancels a stock movement')
def cancel_stock_movement(id: int, db: Session = Depends(get_db)):
    canceled_sotck_movement = cancel_stock_movement_service(db, id)
    if not canceled_sotck_movement:
        raise HTTPException(status_code=400, detail='Stock movement was not canceled')
    return canceled_sotck_movement
