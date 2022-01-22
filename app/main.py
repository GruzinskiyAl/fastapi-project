from typing import Optional, List, Dict

from fastapi import (FastAPI, Query, Path, Body, Cookie,
                     Header, Form, status, File, UploadFile)
from .models import Task

app = FastAPI()

tasks: Dict[int, Task] = {
    1: Task(pk=1, name='Test')
}


@app.post('/files/')
async def create_file(file: bytes = File(...)):
    return {'file_size': len(file)}


@app.post('/uploadfile/')
async def create_upload_file(files: List[UploadFile] = File(...)):
    return {'file_name': 'filw'}


@app.post('/login/')
async def login(username: str = Form(...), password: str = Form(...)):
    return {'username': username}


@app.get("/tasks/", response_model=List[Task])
async def task_list(
        filter_str: str = Query(None, min_length=3, title='Filter', alias='filter'),
        some_id: Optional[str] = Cookie(None),
        user_agent: str = Header(None)
):
    if filter_str:
        return filter(lambda x: filter_str in x.name, tasks.values())
    return list(tasks.values())


@app.post(
    '/tasks',
    status_code=status.HTTP_201_CREATED,
    response_model=List[Task]
)
async def create_tasks(
        new_tasks: List[Task] = Body(..., alias='tasks')
):
    for task in new_tasks:
        tasks[task.pk] = task
    return new_tasks


@app.get("/tasks/{task_id}/")
async def task_item(
        task_id: int = Path(..., title='Task index', gt=0)):
    return tasks.get(task_id)


@app.put("/tasks/{task_id}/")
async def update_task_item(
        task: Task,
        task_id: int = Path(..., title='Task index', gt=0),
):
    tasks.update({task_id: task})
    return task
