from src.models.product_model import Product, ProductCreate, ProductUpdate
from typing import List
from fastapi import Path, Query, APIRouter
from fastapi.responses import JSONResponse

products: List[Product] = []

product_router = APIRouter()

@product_router.get('/product', status_code = 200, response_description = 'Respuesta exitosa') #tag='Product', 
def get_products() -> Product:
    if products: 
        response = [product.model_dump() for product in products]
        return JSONResponse(content = response, status_code = 200)
    else:
        return JSONResponse(content = {}, status_code = 404)

@product_router.get('/product/{id}', status_code = 200, response_description = 'Se obtuvo el producto')
def get_product_by_id(id: int) -> Product:
    if products:
        None #response = product.model_dump() for product in products if product.id == id
        return
    else:
        None
        return