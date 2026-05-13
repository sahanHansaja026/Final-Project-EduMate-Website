from pydantic import BaseModel
from datetime import datetime


class QuizScoreCreate(BaseModel):
    quiz_id: int
    student_id: int
    attempt_number: int = 1
    total_marks: float
    obtained_marks: float
    percentage: float
    correct_answers: int
    wrong_answers: int
    skipped_answers: int
    status: str = "completed"


class QuizScoreResponse(QuizScoreCreate):
    id: int
    started_at: datetime
    submitted_at: datetime

    class Config:
        from_attributes = True