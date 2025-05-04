"""
Объединение остальных файлов, регистрация всех эндпоинтов
"""
from typing import List
from fastapi import FastAPI, Depends, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from .database import engine, get_db
from .models import Base
from .schemas import UserCreate, User, Token, TaskCreate, Task, TaskUpdate, TaskAssignment
from .schemas import TaskAssignmentRequest
from .crud import get_user_by_email, user_create, get_tasks, create_user_task, get_task
from .crud import task_update, task_delete
from .auth import get_current_user, create_access_token, authenticate_user
from .algorithms import optimal_task_assignment

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/token", response_model=Token)
async def login_for_access_token(
    email: str = Form(...),
    password: str = Form(...)
):
    """
    Эндпоинт POST /token
    """
    user = authenticate_user(email, password)  # Передаем email вместо username
    if not user:
        raise HTTPException(
            status_code=400,
            detail="Incorrect email or password"
        )
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/users/", response_model=User)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """
    Эндпоинт POST /users/
    """
    db_user = get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return user_create(db=db, user=user)

@app.get("/users/me/", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_user)):
    """
    Эндпоинт GET /users/me/
    """
    return current_user

@app.post("/tasks/", response_model=Task)
def create_task(
    task: TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Эндпоинт POST /tasks/
    """
    return create_user_task(db=db, task=task, user_id=current_user.id)

@app.get("/tasks/", response_model=List[Task])
def read_tasks(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Эндпоинт GET /tasks/
    """
    tasks = get_tasks(db, owner_id=current_user.id, skip=skip, limit=limit)
    return tasks

@app.get("/tasks/{task_id}", response_model=Task)
def read_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Эндпоинт GET /tasks/{id} 
    """
    db_task = get_task(db, task_id=task_id)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    if db_task.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to access this task")
    return db_task

@app.put("/tasks/{task_id}", response_model=Task)
def update_task(
    task_id: int,
    task: TaskUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Эндпоинт PUT /tasks/{id} 
    """
    db_task = get_task(db, task_id=task_id)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    if db_task.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to update this task")
    return task_update(db=db, task_id=task_id, task=task)

@app.delete("/tasks/{task_id}", response_model=Task)
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Эндпоинт DELETE /tasks/{id}
    """
    db_task = get_task(db, task_id=task_id)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    if db_task.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this task")
    return task_delete(db=db, task_id=task_id)

@app.post("/tasks/assign/optimal", response_model=List[TaskAssignment])
def assign_tasks_optimally(
    assignment_request: TaskAssignmentRequest,
    db: Session = Depends(get_db)
):
    """
    Эндпоинт POST /tasks/assign/optimal
    """
    return optimal_task_assignment(db, assignment_request)
