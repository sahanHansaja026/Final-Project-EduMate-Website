from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class OptionCreate(BaseModel):
    option_text: str
    is_correct: bool = False


class OptionResponse(OptionCreate):
    id: int

    class Config:
        from_attributes = True


class QuestionCreate(BaseModel):
    quiz_id: int

    question_number: int

    question_type: str

    question_text: str

    marks: int = 1

    explanation: Optional[str] = None

    difficulty: Optional[str] = "medium"

    is_required: bool = True

    allow_negative_marking: bool = False

    negative_marks: int = 0

    options: Optional[List[OptionCreate]] = []


class QuestionResponse(QuestionCreate):
    id: int

    created_at: datetime

    updated_at: datetime

    options: List[OptionResponse]

    class Config:
        from_attributes = True