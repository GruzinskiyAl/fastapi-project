from sqlalchemy.orm import Session

from . import models, schemas


def hash_password(password: str) -> str:
    return password + 'pseudohash'


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, offset: int, limit: int):
    return db.query(models.User).offset(offset).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = hash_password(user.password)
    db_user = models.User(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_tasks(db: Session, offset: int, limit: int) -> list[models.Task]:
    return db.query(models.Task).offset(offset).limit(limit).all()


def create_task(db: Session, task: schemas.TaskCreate, user_id: int) -> models.Task:
    db_task = models.Task(**task.dict(), user_id=user_id)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task
