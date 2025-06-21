from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from src.schemas.product_schema import ProductResponse, ProductCreate, ProductUpdate
from src.database.database import get_db
from src.services.product_service import (
    get_all_products as get_all_products_service, 
    create_product as create_product_service,
    update_product as update_product_service,
    desable_product as desable_product_service)

product_router = APIRouter()

@product_router.get('/products', status_code=200, response_model=List[ProductResponse],  response_description = 'List of available products')
def get_products(db: Session = Depends(get_db)):
    products = get_all_products_service(db)
    if not products: 
       raise HTTPException(status_code=404, detail="No products found")
    return products

@product_router.get('/products/{id}', status_code=200, response_model=ProductResponse, summary="Get a product by id", response_description='Returns a product if it exists')
def get_product_by_id(id: int, db: Session = Depends(get_db)):
    product = get_product_by_id(db, id)
    if not product:
        raise HTTPException(status_code=404, detail='Product not found')
    return product

@product_router.post('/products', status_code=201, response_model=ProductResponse, summary='Create a new product', response_description='Adds a new product to the database')
def create_product(new_product: ProductCreate, db: Session = Depends(get_db)):
    product = create_product_service(db, new_product)
    if not product:
        raise HTTPException(status_code=404,detail='Product could not be created')
    return product

@product_router.put('/products/{id}', status_code=200, response_model=ProductResponse, summary='Update the information of a product', response_description='Updates the product with the specified ID')
def update_product(id: int, product_data: ProductUpdate, db: Session = Depends(get_db)):
    product = update_product_service(db, id, product_data)
    if not product:
        raise HTTPException(status_code=404,detail='Product not found')
    return product

@product_router.delete('/products/{id}', status_code=200, response_model=ProductResponse, summary='Delete the product', response_description='Logically deletes the product with the specified ID')
def delete_product(id:int, db: Session = Depends(get_db)):
    product = desable_product_service(db, id)
    if not product:
        raise HTTPException(status_code=404,detail='Product not found')
    return product