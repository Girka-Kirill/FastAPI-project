"""
Операции с БД для управления пользователями и задачами
"""

from sqlalchemy.orm import Session
from passlib.context import CryptContext
from .models import User, Task
from .schemas import UserCreate, TaskCreate, TaskUpdate

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# User CRUD operations
def get_user(db: Session, user_id: int):
    """
    Операция чтения пользователя по ID
    """
    return db.query(User).filter(User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    """
    Операция чтения пользователя по почтовому адресу
    """
    return db.query(User).filter(User.email == email).first()

def user_create(db: Session, user: UserCreate):
    """
    Операция создания нового пользователя
    """
    hashed_password = pwd_context.hash(user.password)
    db_user = User(
        email=user.email,
        hashed_password=hashed_password,
        full_name=user.full_name
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Task CRUD operations
def get_task(db: Session, task_id: int):
    """
    Операция чтения задачи по ID
    """
    return db.query(Task).filter(Task.id == task_id).first()

def get_tasks(db: Session, owner_id: int, skip: int = 0, limit: int = 100):
    """
    Операция чтения нескольких задач
    """
    return db.query(Task).filter(Task.owner_id == owner_id).offset(skip).limit(limit).all()

def create_user_task(db: Session, task: TaskCreate, user_id: int):
    """
    Операция создания задачи
    """
    db_task = Task(**task.dict(), owner_id=user_id)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

def task_update(db: Session, task_id: int, task: TaskUpdate):
    """
    Операция редактирования задачи
    """
    db_task = db.query(Task).filter(Task.id == task_id).first()
    if db_task is None:
        return None
    for field, value in task.dict(exclude_unset=True).items():
        setattr(db_task, field, value)
    db.commit()
    db.refresh(db_task)
    return db_task

def task_delete(db: Session, task_id: int):
    """
    Операция удаления задачи
    """
    db_task = db.query(Task).filter(Task.id == task_id).first()
    if db_task is None:
        return None
    db.delete(db_task)
    db.commit()
    return db_task
