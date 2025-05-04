"""
Pydantic схемы для работы с эндпоинтами
"""
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, EmailStr

# Auth models
class Token(BaseModel):
    """
    Схема Token
    """
    access_token: str
    token_type: str

class TokenRequestForm(BaseModel):
    """
    Схема TokenRequestForm
    """
    email: EmailStr
    password: str
    grant_type: str = "password"
    scope: str = ""

class TokenData(BaseModel):
    """
    Схема TokenData 
    """
    email: Optional[str] = None

class UserLogin(BaseModel):
    """
    Схема UserLogin 
    """
    email: EmailStr
    password: str

# User models
class UserBase(BaseModel):
    """
    Схема UserBase 
    """
    email: EmailStr
    full_name: Optional[str] = None

class UserCreate(UserBase):
    """
    Схема UserCreate
    """
    password: str

class User(UserBase):
    """
    Схема User 
    """
    id: int
    is_active: bool

    class Config:
        """
        Класс для хранения опции orm_mode 
        """
        orm_mode = True

# Task models
class TaskBase(BaseModel):
    """
    Схема TaskBase 
    """
    title: str
    description: Optional[str] = None
    status: str = "open"
    priority: int = 1

class TaskCreate(TaskBase):
    """
    Схема TaskCreate
    """
    pass

class TaskUpdate(TaskBase):
    """
    Схема TaskUpdate 
    """
    pass

class Task(TaskBase):
    """
    Схема Task 
    """
    id: int
    owner_id: int
    created_at: datetime
    due_date: Optional[datetime] = None

    class Config:
        """
        Класс для хранения опции orm_mode 
        """
        orm_mode = True

# Assignment models
class TaskAssignment(BaseModel):
    """
    Схема TaskAssignment 
    """
    task_id: int
    user_id: int
    score: float
    assigned_skills: List[str]

class TaskAssignmentRequest(BaseModel):
    """
    Схема TaskAssignmenRequest 
    """
    task_ids: List[int]
