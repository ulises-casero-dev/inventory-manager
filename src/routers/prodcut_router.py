from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from src.schemas.product_schema import ProductResponse
from src.database.database import get_db
from src.services.product_service import get_all_products

product_router = APIRouter()

@product_router.get('/products', status_code = 200, response_model=List[ProductResponse],  response_description = 'List of available products')
def get_products(db: Session = Depends(get_db)):
    products = get_all_products(db)
    if not products: 
       raise HTTPException(status_code=404, detail="No products found")
    else:
        return products

@product_router.get('/products/{id}', status_code = 200, response_model=ProductResponse, summary="Get a product by id", response_description = 'Returns a product if it exists')
def get_product_by_id(id: int, db: Session = Depends(get_db)):
    product = get_product_by_id(db, id)
    if not product:
        return HTTPException(status_code=404, detail='Producto not found')
    else:
        return product