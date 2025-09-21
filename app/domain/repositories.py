from abc import ABC, abstractmethod
from typing import List, Optional

from domain.models import Task, TaskHistoryRecord


class TaskRepository(ABC):
    """Абстрактный репозиторий для работы с задачами"""
    
    @abstractmethod
    async def create(self, task: Task) -> Task:
        pass
    
    @abstractmethod
    async def get_by_id(self, task_id: str) -> Optional[Task]:
        pass
    
    @abstractmethod
    async def get_all(self, status: Optional[str] = None) -> List[Task]:
        pass
    
    @abstractmethod
    async def update_status(self, task_id: str, status: str) -> Optional[Task]:
        pass
    
    @abstractmethod
    async def assign_task(self, task_id: str, assigned_to: str) -> Optional[Task]:
        pass
    
    @abstractmethod
    async def rate_task(self, task_id: str, rating: int, comment: Optional[str]) -> bool:
        pass


class TaskHistoryRepository(ABC):
    """Абстрактный репозиторий для работы с историей задач"""
    
    @abstractmethod
    async def create_record(self, record: TaskHistoryRecord) -> None:
        pass
    
    @abstractmethod
    async def get_task_history(self, task_id: str) -> List[dict]:
        pass