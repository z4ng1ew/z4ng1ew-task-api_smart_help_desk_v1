# В данном случае схемы уже определены в domain/models.py
# Если нужны отдельные схемы для API, можно добавить их здесь

from domain.models import (
    Task,
    TaskCreate,
    TaskStatusUpdate,
    TaskAssignment,
    TaskRating
)

# Экспортируем схемы для использования в роутерах
__all__ = [
    "Task",
    "TaskCreate", 
    "TaskStatusUpdate",
    "TaskAssignment",
    "TaskRating"
]