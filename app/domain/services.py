from datetime import datetime
from typing import List, Optional

from fastapi import HTTPException

from core.config import settings
from domain.models import (
    Task, TaskCreate, TaskHistoryRecord, 
    generate_task_id, calculate_due_date
)
from domain.repositories import TaskRepository, TaskHistoryRepository


class TaskService:
    def __init__(
        self, 
        task_repo: TaskRepository, 
        history_repo: TaskHistoryRepository
    ):
        self.task_repo = task_repo
        self.history_repo = history_repo
    
    async def create_task(self, task_data: TaskCreate, created_by: str) -> Task:
        """Создание новой задачи"""
        task_id = generate_task_id()
        due_date = calculate_due_date(task_data.priority)
        
        task = Task(
            id=task_id,
            **task_data.model_dump(),
            status="new",
            created_by=created_by,
            created_at=datetime.now(),
            due_date=due_date
        )
        
        # Сохраняем задачу
        created_task = await self.task_repo.create(task)
        
        # Создаем запись в истории
        history_record = TaskHistoryRecord(
            task_id=task_id,
            action="created",
            performed_by=created_by,
            details={
                "title": task_data.title,
                "category": task_data.category,
                "priority": task_data.priority
            },
            timestamp=datetime.now()
        )
        await self.history_repo.create_record(history_record)
        
        return created_task
    
    async def get_task(self, task_id: str) -> Task:
        """Получение задачи по ID"""
        task = await self.task_repo.get_by_id(task_id)
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        return task
    
    async def list_tasks(self, status: Optional[str] = None) -> List[Task]:
        """Получение списка задач"""
        return await self.task_repo.get_all(status)
    
    async def update_task_status(
        self, 
        task_id: str, 
        new_status: str, 
        performed_by: str
    ) -> Task:
        """Обновление статуса задачи"""
        if new_status not in settings.valid_transitions:
            raise HTTPException(status_code=400, detail="Invalid status")
        
        # Получаем текущую задачу
        current_task = await self.task_repo.get_by_id(task_id)
        if not current_task:
            raise HTTPException(status_code=404, detail="Task not found")
        
        current_status = current_task.status
        
        # Проверяем валидность перехода
        if new_status not in settings.valid_transitions.get(current_status, []):
            raise HTTPException(
                status_code=400,
                detail=f"Invalid status transition from '{current_status}' to '{new_status}'"
            )
        
        # Обновляем статус
        updated_task = await self.task_repo.update_status(task_id, new_status)
        if not updated_task:
            raise HTTPException(status_code=404, detail="Task not found or status not changed")
        
        # Создаем запись в истории
        history_record = TaskHistoryRecord(
            task_id=task_id,
            action="status_changed",
            from_status=current_status,
            to_status=new_status,
            performed_by=performed_by,
            timestamp=datetime.now()
        )
        await self.history_repo.create_record(history_record)
        
        return updated_task
    
    async def assign_task(
        self, 
        task_id: str, 
        assigned_to: str, 
        performed_by: str
    ) -> Task:
        """Назначение исполнителя"""
        # Получаем текущую задачу
        current_task = await self.task_repo.get_by_id(task_id)
        if not current_task:
            raise HTTPException(status_code=404, detail="Task not found")
        
        # Назначаем исполнителя
        updated_task = await self.task_repo.assign_task(task_id, assigned_to)
        if not updated_task:
            raise HTTPException(status_code=404, detail="Task not found")
        
        # Создаем запись в истории
        history_record = TaskHistoryRecord(
            task_id=task_id,
            action="assigned",
            previous_assignee=current_task.assigned_to,
            new_assignee=assigned_to,
            performed_by=performed_by,
            timestamp=datetime.now()
        )
        await self.history_repo.create_record(history_record)
        
        return updated_task
    
    async def rate_task(
        self, 
        task_id: str, 
        rating: int, 
        comment: Optional[str], 
        performed_by: str
    ) -> dict:
        """Оценка задачи"""
        # Проверяем, что задача существует и завершена
        task = await self.task_repo.get_by_id(task_id)
        if not task or task.status not in ["completed", "closed"]:
            raise HTTPException(
                status_code=400, 
                detail="Can only rate completed or closed tasks"
            )
        
        # Сохраняем оценку
        success = await self.task_repo.rate_task(task_id, rating, comment)
        if not success:
            raise HTTPException(status_code=500, detail="Failed to save rating")
        
        # Создаем запись в истории
        history_record = TaskHistoryRecord(
            task_id=task_id,
            action="rated",
            rating=rating,
            comment=comment,
            performed_by=performed_by,
            timestamp=datetime.now()
        )
        await self.history_repo.create_record(history_record)
        
        return {"task_id": task_id, "rating": rating, "comment": comment}
    
    async def get_task_history(self, task_id: str) -> dict:
        """Получение истории задачи"""
        history = await self.history_repo.get_task_history(task_id)
        return {"task_id": task_id, "history": history}