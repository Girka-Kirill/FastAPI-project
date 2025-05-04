"""
Подключение к БД и создание сессий
"""
import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


# Создаем директорию для базы данных, если ее нет
os.makedirs("databases", exist_ok=True)

SQLALCHEMY_DATABASE_URL = "sqlite:///databases/task_manager.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    """
    Получение доступа к используемой базе данных
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
