from fastapi import FastAPI
from src.routers import all_routers
from src.exceptions.handlers import register_exception_handlers

def create_app() -> FastAPI:
    app = FastAPI()

    register_exception_handlers(app)

    for router in all_routers:
        app.include_router(router)

    return app
