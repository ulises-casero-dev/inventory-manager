from fastapi import FastAPI
from src.routers.product_router import product_router
from src.routers.category_router import category_router
from src.routers.stock_router import stock_router


app = FastAPI()

app.include_router(product_router)
app.include_router(category_router)
app.include_router(stock_router)