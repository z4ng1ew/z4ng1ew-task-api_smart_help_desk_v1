from motor.motor_asyncio import AsyncIOMotorClient
from core.config import settings


class DatabaseManager:
    client: AsyncIOMotorClient = None
    database = None


db_manager = DatabaseManager()


async def connect_to_mongo():
    """Создает соединение с MongoDB"""
    db_manager.client = AsyncIOMotorClient(settings.mongo_url)
    db_manager.database = db_manager.client.get_database()


async def close_mongo_connection():
    """Закрывает соединение с MongoDB"""
    if db_manager.client:
        db_manager.client.close()


def get_database():
    """Получает экземпляр базы данных"""
    return db_manager.database