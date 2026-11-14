from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class SubmissionResponse(BaseModel):
    id: int
    assignment_id: int
    student_id: int
    file_path: str
    submitted_at: datetime
    marks: Optional[int]
    feedback: Optional[str]

    class Config:
        from_attributes = True

class GradeUpdate(BaseModel):
    marks: Optional[int] = None
