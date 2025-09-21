from ..core.database import db as core_db
from .repositories import MongoTaskRepository
from ..domain.repositories import TaskRepository

class Database:
    def __init__(self):
        self.db = core_db

    def get_task_repository(self) -> TaskRepository:
        return MongoTaskRepository(self.db.get_db().tasks)