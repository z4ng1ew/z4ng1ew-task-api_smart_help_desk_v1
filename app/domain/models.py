import uuid
from datetime import datetime, timedelta
from typing import List, Optional
from pydantic import BaseModel, Field

from core.config import settings


class TaskCreate(BaseModel):
    title: str
    description: str
    category: str  # electrical, plumbing, repair, etc.
    location_id: str
    priority: str  # low, medium, high, critical


class Task(BaseModel):
    id: str
    title: str
    description: str
    category: str
    location_id: str
    priority: str
    status: str = "new"  # new → assigned → in_progress → completed → closed
    created_by: str
    assigned_to: Optional[str] = None
    created_at: datetime
    due_date: Optional[datetime] = None
    attachments: List[str] = []
    rating: Optional[int] = None
    rating_comment: Optional[str] = None


class TaskStatusUpdate(BaseModel):
    status: str


class TaskAssignment(BaseModel):
    assigned_to: str


class TaskRating(BaseModel):
    rating: int = Field(..., ge=1, le=5)
    comment: Optional[str] = None


class TaskHistoryRecord(BaseModel):
    task_id: str
    action: str
    performed_by: str
    timestamp: datetime
    details: Optional[dict] = None
    from_status: Optional[str] = None
    to_status: Optional[str] = None
    previous_assignee: Optional[str] = None
    new_assignee: Optional[str] = None
    rating: Optional[int] = None
    comment: Optional[str] = None


def generate_task_id() -> str:
    """Генерирует уникальный ID для задачи"""
    return f"T-{datetime.now().strftime('%Y%m%d')}-{str(uuid.uuid4())[:8].upper()}"


def calculate_due_date(priority: str) -> datetime:
    """Вычисляет срок выполнения на основе приоритета"""
    hours = settings.priority_hours.get(priority, 24)
    return datetime.now() + timedelta(hours=hours)