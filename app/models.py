from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, func
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    tasks = relationship('Task', back_populates='user')


class Task(Base):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    created = Column(DateTime, server_default=func.now())
    title = Column(String, index=True)
    description = Column(String, nullable=True)
    is_done = Column(Boolean, default=False)

    user = relationship('User', back_populates='tasks')
