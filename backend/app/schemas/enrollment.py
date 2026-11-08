from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class EnrollmentCreate(BaseModel):
    user_id: int
    module_id: int


class EnrollmentUpdate(BaseModel):
    completed: bool


class EnrollmentResponse(BaseModel):
    enrollment_id: int
    user_id: int
    module_id: int
    enrolled_at: datetime
    completed: bool

    class Config:
        from_attributes = True