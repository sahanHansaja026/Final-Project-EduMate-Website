from pydantic import BaseModel
from typing import Optional


class ManualGradeResponse(BaseModel):
    question_id: int
    question_text: str
    question_marks: float
    student_answer: Optional[str]
    score: float

    class Config:
        from_attributes = True


class ManualGradeUpdate(BaseModel):
    quiz_id: int
    student_id: int
    question_id: int
    score: float