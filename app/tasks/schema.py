from datetime import date
from enum import Enum
from pydantic import BaseModel, EmailStr, Field


class Priority(Enum):
    LOW = 'low'
    MEDIUM = 'medium'
    HIGH = 'high'


class STasks(BaseModel):
    
    id: int
    title: str = Field(max_length=100)
    description: str
    due_data: date
    is_completed: bool
    priority: Priority
    user_id: int
    
    
    
    class ConfigDict:
        from_attributes = True