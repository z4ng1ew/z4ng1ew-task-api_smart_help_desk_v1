from typing import List, Optional

from core.database import get_database
from domain.models import Task, TaskHistoryRecord
from domain.repositories import TaskRepository, TaskHistoryRepository


class MongoTaskRepository(TaskRepository):
    def __init__(self):
        self.database = get_database()
        self.collection = self.database["tasks"]
    
    async def create(self, task: Task) -> Task:
        await self.collection.insert_one(task.model_dump())
        return task
    
    async def get_by_id(self, task_id: str) -> Optional[Task]:
        task_data = await self.collection.find_one({"id": task_id})
        if task_data:
            return Task(**task_data)
        return None
    
    async def get_all(self, status: Optional[str] = None) -> List[Task]:
        query = {}
        if status:
            query["status"] = status
        
        cursor = self.collection.find(query)
        tasks_data = await cursor.to_list(length=100)
        return [Task(**task_data) for task_data in tasks_data]
    
    async def update_status(self, task_id: str, status: str) -> Optional[Task]:
        result = await self.collection.update_one(
            {"id": task_id},
            {"$set": {"status": status}}
        )
        
        if result.modified_count == 0:
            return None
        
        return await self.get_by_id(task_id)
    
    async def assign_task(self, task_id: str, assigned_to: str) -> Optional[Task]:
        result = await self.collection.update_one(
            {"id": task_id},
            {"$set": {"status": "assigned", "assigned_to": assigned_to}}
        )
        
        if result.modified_count == 0:
            return None
        
        return await self.get_by_id(task_id)
    
    async def rate_task(self, task_id: str, rating: int, comment: Optional[str]) -> bool:
        result = await self.collection.update_one(
            {"id": task_id},
            {"$set": {"rating": rating, "rating_comment": comment}}
        )
        return result.modified_count > 0


class MongoTaskHistoryRepository(TaskHistoryRepository):
    def __init__(self):
        self.database = get_database()
        self.collection = self.database["task_history"]
    
    async def create_record(self, record: TaskHistoryRecord) -> None:
        await self.collection.insert_one(record.model_dump())
    
    async def get_task_history(self, task_id: str) -> List[dict]:
        cursor = self.collection.find({"task_id": task_id}).sort("timestamp", -1)
        history = await cursor.to_list(length=100)
        
        # Удаляем _id для чистоты JSON
        for record in history:
            record.pop("_id", None)
        
        return history