from pydantic import BaseModel
from typing import Optional


class StudentAnswerCreate(BaseModel):
    quiz_id: int
    question_id: int
    student_id: int
    selected_option_id: Optional[int] = None
    answer_text: Optional[str] = None
    is_correct: bool
    obtained_marks: float


class StudentAnswerResponse(StudentAnswerCreate):
    id: int

    class Config:
        from_attributes = True