"""
SQLAlchemy модели для хранения таблиц БД
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class User(Base):
    """
    Модель User
    """
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    full_name = Column(String)
    is_active = Column(Boolean, default=True)
    tasks = relationship("Task", back_populates="owner")
    skills = relationship("UserSkill", back_populates="user")
class Task(Base):
    """
    Модель Task
    """
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    status = Column(String, default="open")
    priority = Column(Integer, default=1)
    created_at = Column(DateTime, default=datetime.utcnow)
    due_date = Column(DateTime, nullable=True)
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="tasks")
    required_skills = relationship("TaskSkill", back_populates="task")
class UserSkill(Base):
    """
    Модель UserSkill 
    """
    __tablename__ = "user_skills"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    skill_id = Column(Integer, ForeignKey("skills.id"))
    level = Column(Integer, default=1)
    user = relationship("User", back_populates="skills")
    skill = relationship("Skill", back_populates="user_skills")
class Skill(Base):
    """
    Модель Skill 
    """
    __tablename__ = "skills"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    description = Column(String)
    user_skills = relationship("UserSkill", back_populates="skill")
    task_skills = relationship("TaskSkill", back_populates="skill")
class TaskSkill(Base):
    """
    Модель TaskSkill 
    """
    __tablename__ = "task_skills"
    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(Integer, ForeignKey("tasks.id"))
    skill_id = Column(Integer, ForeignKey("skills.id"))
    required_level = Column(Integer, default=1)
    task = relationship("Task", back_populates="required_skills")
    skill = relationship("Skill", back_populates="task_skills")
    