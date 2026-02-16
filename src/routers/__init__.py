from src.routers.user_router import user_router
from src.routers.product_router import product_router
from src.routers.category_router import category_router
from src.routers.purchase_router import purchase_router
from src.routers.purchase_item_router import purchase_item_router
from src.routers.stock_router import stock_router
#from src.routers.stock_movement_router import 

all_routers = [
    user_router,
    product_router,
    category_router,
    purchase_router,
    purchase_item_router,
    stock_router
]