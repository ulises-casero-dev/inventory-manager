from fastapi.responses import JSONResponse
from datetime import datetime

from src.exceptions.custom_exceptions import ConflictException

def register_exception_handlers(app):
    @app.exception_handler(ConflictException)
    async def conflict_handler(request, exc: ConflictException):
        return JSONResponse(
            status_code=409,
            content={
                "error": {
                    "code": exc.error_code,
                    "message": exc.message,
                    "timestamp": datetime.utcnow().isoformat()
                }
            }
        )
