from src.routers.user_router import user_router
from src.routers.product_router import product_router
from src.routers.category_router import category_router
from src.routers.order_router import order_router
from src.routers.order_item_router import order_item_router
from src.routers.stock_router import stock_router

all_routers = [
    user_router,
    product_router,
    category_router,
    order_router,
    order_item_router,
    stock_router
]