from datetime import date
from typing import Optional

from pydantic import BaseModel, EmailStr


class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None


class TaskCreate(TaskBase):
    pass


class Task(TaskBase):
    id: int
    user_id: int
    created: date
    is_done: bool

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool
    tasks: list[Task] = []

    class Config:
        orm_mode = True
