from datetime import date
from enum import Enum
from pydantic import BaseModel, EmailStr, Field
from typing import Optional


class Priority(Enum):
    LOW = 'low'
    MEDIUM = 'medium'
    HIGH = 'high'


class STasks(BaseModel):
    
    title: str = Field(max_length=100)
    description: Optional[str] = None
    due_data: Optional[date] = None
    is_completed: bool = False
    priority: Priority = Priority.MEDIUM
    
    
    
    class ConfigDict:
        from_attributes = True