from fastapi import Depends

# Импортируем модуль авторизации (предполагается, что он есть)
from auth import verify_token

from domain.services import TaskService
from infrastructure.repositories import MongoTaskRepository, MongoTaskHistoryRepository


def get_task_repository() -> MongoTaskRepository:
    """Dependency для получения репозитория задач"""
    return MongoTaskRepository()


def get_history_repository() -> MongoTaskHistoryRepository:
    """Dependency для получения репозитория истории"""
    return MongoTaskHistoryRepository()


def get_task_service(
    task_repo: MongoTaskRepository = Depends(get_task_repository),
    history_repo: MongoTaskHistoryRepository = Depends(get_history_repository)
) -> TaskService:
    """Dependency для получения сервиса задач"""
    return TaskService(task_repo, history_repo)


def get_current_user(payload: dict = Depends(verify_token)) -> dict:
    """Dependency для получения текущего пользователя из токена"""
    return payload