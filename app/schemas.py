from typing import List, Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime

# Auth models
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenRequestForm(BaseModel):
    email: EmailStr 
    password: str
    grant_type: str = "password"
    scope: str = ""
    
class TokenData(BaseModel):
    email: Optional[str] = None

class UserLogin(BaseModel):
    email: EmailStr
    password: str

# User models
class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_active: bool

    class Config:
        orm_mode = True

# Task models
class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    status: str = "open"
    priority: int = 1

class TaskCreate(TaskBase):
    pass

class TaskUpdate(TaskBase):
    pass

class Task(TaskBase):
    id: int
    owner_id: int
    created_at: datetime
    due_date: Optional[datetime] = None

    class Config:
        orm_mode = True

# Assignment models
class TaskAssignment(BaseModel):
    task_id: int
    user_id: int
    score: float
    assigned_skills: List[str]

class TaskAssignmentRequest(BaseModel):
    task_ids: List[int]