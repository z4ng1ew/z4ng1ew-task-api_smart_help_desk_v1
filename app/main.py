from fastapi import FastAPI

from core.config import settings
from core.database import connect_to_mongo, close_mongo_connection
from presentation.routers import router


def create_app() -> FastAPI:
    """Создает и настраивает FastAPI приложение"""
    app = FastAPI(
        title=settings.title,
        version=settings.version
    )
    
    # Подключаем роутеры
    app.include_router(router)
    
    # События запуска и завершения
    @app.on_event("startup")
    async def startup_event():
        await connect_to_mongo()
    
    @app.on_event("shutdown")
    async def shutdown_event():
        await close_mongo_connection()
    
    return app


app = create_app()