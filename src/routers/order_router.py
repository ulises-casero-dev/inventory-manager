from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from src.schemas.order_schema import OrderCreate, OrderUpdate, OrderResponse
from src.database.database import get_db
from src.services.order_service import (
    get_all_orders as get_all_orders_service,
    get_order_by_id as get_order_by_id_service,
    create_order as create_order_service,
    update_order as update_order_service,
    cancel_order as cancel_order_service
)

order_router = APIRouter()

@order_router.get('/orders', status_code=200, response_model=List[OrderResponse], response_description='List of orders')
def get_orders(db: Session = Depends(get_db)):
    orders = get_all_orders_service(db)
    if not orders: 
       raise HTTPException(status_code=404, detail="No orders found")
    return orders

order_router.get('/orders/{id}', status_code=200, response_model=OrderResponse, summary="Get a order by id", response_description='Returns a order if it exists')
def get_order_by_id(id: int, db: Session = Depends(get_db)):
    order = get_order_by_id_service(db, id)
    if not order:
        raise HTTPException(status_code=404)
    return order