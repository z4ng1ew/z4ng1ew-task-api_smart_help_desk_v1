from typing import List, Optional

from fastapi import APIRouter, Depends

from domain.services import TaskService
from presentation.dependencies import get_task_service, get_current_user
from presentation.schemas import (
    Task, TaskCreate, TaskStatusUpdate, 
    TaskAssignment, TaskRating
)

router = APIRouter(prefix="/api/v1", tags=["tasks"])


@router.post("/tasks", response_model=Task)
async def create_task(
    task: TaskCreate,
    service: TaskService = Depends(get_task_service),
    current_user: dict = Depends(get_current_user)
):
    """Создание новой заявки"""
    return await service.create_task(task, current_user["sub"])


@router.get("/tasks/{task_id}", response_model=Task)
async def get_task(
    task_id: str,
    service: TaskService = Depends(get_task_service),
    current_user: dict = Depends(get_current_user)
):
    """Получение заявки по ID"""
    return await service.get_task(task_id)


@router.get("/tasks", response_model=List[Task])
async def list_tasks(
    status: Optional[str] = None,
    service: TaskService = Depends(get_task_service),
    current_user: dict = Depends(get_current_user)
):
    """Список заявок с фильтрацией по статусу"""
    return await service.list_tasks(status)


@router.patch("/tasks/{task_id}/status", response_model=Task)
async def update_task_status(
    task_id: str,
    status_update: TaskStatusUpdate,
    service: TaskService = Depends(get_task_service),
    current_user: dict = Depends(get_current_user)
):
    """Обновление статуса заявки с валидацией переходов"""
    return await service.update_task_status(
        task_id, 
        status_update.status, 
        current_user["sub"]
    )


@router.patch("/tasks/{task_id}/assign", response_model=Task)
async def assign_task(
    task_id: str,
    assignment: TaskAssignment,
    service: TaskService = Depends(get_task_service),
    current_user: dict = Depends(get_current_user)
):
    """Назначение исполнителя (автоматически меняет статус на 'assigned')"""
    return await service.assign_task(
        task_id, 
        assignment.assigned_to, 
        current_user["sub"]
    )


@router.get("/tasks/{task_id}/history")
async def get_task_history(
    task_id: str,
    service: TaskService = Depends(get_task_service),
    current_user: dict = Depends(get_current_user)
):
    """Получение истории изменений заявки"""
    return await service.get_task_history(task_id)


@router.post("/tasks/{task_id}/rating")
async def rate_task(
    task_id: str,
    rating_data: TaskRating,
    service: TaskService = Depends(get_task_service),
    current_user: dict = Depends(get_current_user)
):
    """Оценка выполненной заявки"""
    return await service.rate_task(
        task_id, 
        rating_data.rating, 
        rating_data.comment,
        current_user["sub"]
    )