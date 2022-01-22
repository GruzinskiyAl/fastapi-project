from datetime import date
from typing import Optional

from pydantic import BaseModel, Field


class Task(BaseModel):
    pk: int = Field(..., description='Primary Key', gt=0)
    name: str
    effective_date: Optional[date] = None
    is_done: bool = False
    description: Optional[str] = None
