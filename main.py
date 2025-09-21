import os
import uuid
from datetime import datetime, timedelta
from typing import List, Optional

from fastapi import FastAPI, HTTPException, Depends
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel

# Импорт модуля авторизации
from auth import verify_token

app = FastAPI(title="Task Service", version="0.1.0")

# Подключение к MongoDB
MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017/helpdesk")
client = AsyncIOMotorClient(MONGO_URL)
database = client.get_database()
tasks_collection = database["tasks"]
history_collection = database["task_history"]  # Коллекция для истории изменений

# Модель заявки
class TaskCreate(BaseModel):
    title: str
    description: str
    category: str  # electrical, plumbing, repair, etc.
    location_id: str
    priority: str  # low, medium, high, critical

class Task(TaskCreate):
    id: str
    status: str = "new"  # new → assigned → in_progress → completed → closed
    created_by: str
    assigned_to: Optional[str] = None
    created_at: datetime
    due_date: Optional[datetime] = None
    attachments: List[str] = []

# Определяем допустимые переходы статусов
VALID_TRANSITIONS = {
    "new": ["assigned", "rejected"],
    "assigned": ["in_progress", "rejected"],
    "in_progress": ["completed", "rejected"],
    "completed": ["closed", "rejected"],
    "closed": [],
    "rejected": []
}

@app.post("/api/v1/tasks", response_model=Task)
async def create_task(
    task: TaskCreate,
    payload: dict = Depends(verify_token)  # Получаем пользователя из токена
):
    """Создание новой заявки"""
    task_id = f"T-{datetime.now().strftime('%Y%m%d')}-{str(uuid.uuid4())[:8].upper()}"
    
    # Расчет due_date по приоритету
    hours = {"low": 72, "medium": 24, "high": 4, "critical": 1}
    due_date = datetime.now() + timedelta(hours=hours.get(task.priority, 24))

    new_task = Task(
        id=task_id,
        **task.model_dump(),
        status="new",
        created_by=payload["sub"],  # Берем user ID из токена
        created_at=datetime.now(),
        due_date=due_date
    )
    
    # Сохраняем в MongoDB
    await tasks_collection.insert_one(new_task.model_dump())
    
    # Логируем создание заявки в истории
    await history_collection.insert_one({
        "task_id": task_id,
        "action": "created",
        "performed_by": payload["sub"],
        "details": {
            "title": task.title,
            "category": task.category,
            "priority": task.priority
        },
        "timestamp": datetime.now()
    })
    
    return new_task

@app.get("/api/v1/tasks/{task_id}", response_model=Task)
async def get_task(
    task_id: str,
    payload: dict = Depends(verify_token)  # Защищаем эндпоинт
):
    """Получение заявки по ID"""
    task = await tasks_collection.find_one({"id": task_id})
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return Task(**task)

@app.get("/api/v1/tasks", response_model=List[Task])
async def list_tasks(
    status: Optional[str] = None,
    payload: dict = Depends(verify_token)  # Защищаем эндпоинт
):
    """Список заявок с фильтрацией по статусу"""
    query = {}
    if status:
        query["status"] = status
    cursor = tasks_collection.find(query)
    tasks = await cursor.to_list(length=100)
    return [Task(**task) for task in tasks]

@app.patch("/api/v1/tasks/{task_id}/status", response_model=Task)
async def update_task_status(
    task_id: str,
    status: str,
    payload: dict = Depends(verify_token)  # Защищаем эндпоинт
):
    """Обновление статуса заявки с валидацией переходов"""
    if status not in VALID_TRANSITIONS:
        raise HTTPException(status_code=400, detail="Invalid status")
    
    # Получаем текущую заявку
    current_task = await tasks_collection.find_one({"id": task_id})
    if not current_task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    current_status = current_task["status"]
    
    # Проверяем валидность перехода
    if status not in VALID_TRANSITIONS.get(current_status, []):
        raise HTTPException(
            status_code=400,
            detail=f"Invalid status transition from '{current_status}' to '{status}'"
        )
    
    # Обновляем статус
    result = await tasks_collection.update_one(
        {"id": task_id},
        {"$set": {"status": status}}
    )
    
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Task not found or status not changed")
    
    # Логируем изменение статуса
    await history_collection.insert_one({
        "task_id": task_id,
        "action": "status_changed",
        "from_status": current_status,
        "to_status": status,
        "performed_by": payload["sub"],
        "timestamp": datetime.now()
    })
    
    updated_task = await tasks_collection.find_one({"id": task_id})
    return Task(**updated_task)

@app.patch("/api/v1/tasks/{task_id}/assign", response_model=Task)
async def assign_task(
    task_id: str,
    assigned_to: str,
    payload: dict = Depends(verify_token)  # Защищаем эндпоинт
):
    """Назначение исполнителя (автоматически меняет статус на 'assigned')"""
    # Получаем текущую заявку
    current_task = await tasks_collection.find_one({"id": task_id})
    if not current_task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    # Обновляем исполнителя и статус
    result = await tasks_collection.update_one(
        {"id": task_id},
        {"$set": {"status": "assigned", "assigned_to": assigned_to}}
    )
    
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Task not found")
    
    # Логируем назначение исполнителя
    await history_collection.insert_one({
        "task_id": task_id,
        "action": "assigned",
        "previous_assignee": current_task.get("assigned_to"),
        "new_assignee": assigned_to,
        "performed_by": payload["sub"],
        "timestamp": datetime.now()
    })
    
    updated_task = await tasks_collection.find_one({"id": task_id})
    return Task(**updated_task)

@app.get("/api/v1/tasks/{task_id}/history")
async def get_task_history(
    task_id: str,
    payload: dict = Depends(verify_token)  # Защищаем эндпоинт
):
    """Получение истории изменений заявки"""
    cursor = history_collection.find({"task_id": task_id}).sort("timestamp", -1)
    history = await cursor.to_list(length=100)
    # Удаляем _id для чистоты JSON
    for record in history:
        record.pop("_id", None)
    return {"task_id": task_id, "history": history}

@app.post("/api/v1/tasks/{task_id}/rating")
async def rate_task(
    task_id: str,
    rating: int,
    comment: Optional[str] = None,
    payload: dict = Depends(verify_token)  # Защищаем эндпоинт
):
    """Оценка выполненной заявки"""
    if not (1 <= rating <= 5):
        raise HTTPException(status_code=400, detail="Rating must be between 1 and 5")
    
    # Проверяем, что заявка в статусе "completed" или "closed"
    task = await tasks_collection.find_one({"id": task_id})
    if not task or task["status"] not in ["completed", "closed"]:
        raise HTTPException(status_code=400, detail="Can only rate completed or closed tasks")
    
    # Обновляем заявку с оценкой (можно также сохранить в отдельную коллекцию)
    await tasks_collection.update_one(
        {"id": task_id},
        {"$set": {"rating": rating, "rating_comment": comment}}
    )
    
    # Логируем оценку
    await history_collection.insert_one({
        "task_id": task_id,
        "action": "rated",
        "rating": rating,
        "comment": comment,
        "performed_by": payload["sub"],
        "timestamp": datetime.now()
    })
    
    return {"task_id": task_id, "rating": rating, "comment": comment}