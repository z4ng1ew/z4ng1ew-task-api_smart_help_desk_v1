import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Database
    mongo_url: str = "mongodb://localhost:27017/helpdesk"
    
    # API
    api_v1_prefix: str = "/api/v1"
    title: str = "Task Service"
    version: str = "0.1.0"
    
    # Task settings
    priority_hours: dict = {
        "low": 72,
        "medium": 24, 
        "high": 4,
        "critical": 1
    }
    
    # Valid status transitions
    valid_transitions: dict = {
        "new": ["assigned", "rejected"],
        "assigned": ["in_progress", "rejected"],
        "in_progress": ["completed", "rejected"],
        "completed": ["closed", "rejected"],
        "closed": [],
        "rejected": []
    }
    
    class Config:
        env_file = ".env"


settings = Settings()