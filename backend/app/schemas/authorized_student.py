from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


class AuthorizedStudentCreate(BaseModel):
    channel_module_id: int
    student_name: str
    student_email: EmailStr
    status: str = "active"
    remark: Optional[str] = None


class AuthorizedStudentUpdate(BaseModel):
    status: Optional[str] = None
    remark: Optional[str] = None


class AuthorizedStudentResponse(BaseModel):
    id: int
    channel_module_id: int
    student_name: str
    student_email: str
    admission_date: datetime
    status: str
    remark: Optional[str]

    class Config:
        from_attributes = True