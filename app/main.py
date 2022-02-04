from typing import Generator

from fastapi import (FastAPI, HTTPException, Depends)
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db() -> Generator:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post('/users/', response_model=schemas.User, tags=['users'])
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail='Email already in use.')
    return crud.create_user(db=db, user=user)


@app.get('/users/', response_model=list[schemas.User], tags=['users'])
def list_users(offset: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_users(db=db, offset=offset, limit=limit)


@app.get('/users/{user_id}/', response_model=schemas.User, tags=['users'])
def get_user(user_id: int, db: Session = Depends(get_db)):
    return crud.get_user(db=db, user_id=user_id)


@app.post('/users/{user_id}/tasks/', response_model=schemas.Task, tags=['users'])
def create_task(
        user_id: int, task: schemas.TaskCreate, db: Session = Depends(get_db)
):
    return crud.create_task(db=db, task=task, user_id=user_id)


@app.get('/tasks/', response_model=schemas.Task, tags=['tasks'])
def list_tasks(offset: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_tasks(db=db, offset=offset, limit=limit)
