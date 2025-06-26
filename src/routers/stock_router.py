from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from src.database.database import get_db
from src.schemas.stock_schema import StockCreate, StockResponse, StockUpdate
from src.services.stock_service import (
    get_all_stocks as get_all_stocks_service,
    get_stock_by_id as get_stock_by_id_service,
    create_stock as create_stock_service,
    update_stock as update_stock_service
)

stock_router = APIRouter(
    prefix="/stocks",
    tags=["Stocks"]
)

@stock_router.get('/stocks', status_code=200, response_model=List[StockResponse], response_description='List of available stock entries')
def get_all_stocks(db: Session = Depends(get_db)):
    stocks = get_all_stocks_service(db)
    if not stocks:
        raise HTTPException(status_code=404, detail='No stock entries found')
    return stocks

@stock_router.get('/stocks/{id}', status_code=200, response_model=StockResponse, summary='Get a stock by id', response_description='Returns a stock if it exists')
def get_stock_by_id(id: int, db: Session = Depends(get_db)):
    stock = get_stock_by_id_service(db, id)
    if not stock:
        raise HTTPException(status_code=404, detail='Stock not found')
    return stock

@stock_router.post('/stocks', status_code=201, response_model=StockResponse, summary='Create a stock entry', response_description='Creates a new stock entry for a product')
def create_stock(stock_data: StockCreate, db: Session = Depends(get_db)):
    new_strock = create_stock_service(db, stock_data)
    if not new_strock:
        raise HTTPException(status_code=404, detail='Stock could not be created')
    return new_strock

@stock_router.put('/stocks/{id}', status_code=200, response_model=StockResponse, summary='Update stock quantity', response_description='Updates the quantity for a specific stock entry')
def update_stock(id: int, stock_data: StockUpdate, db: Session =Depends(get_db)):
    updated_stock = update_stock_service(db, id, stock_data)
    if not updated_stock:
        raise HTTPException(status_code=404, detail='Stock not found')
    return updated_stock