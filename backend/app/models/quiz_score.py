from sqlalchemy import (
    Column,
    Integer,
    Float,
    String,
    DateTime
)

from datetime import datetime
from database import Base


class QuizScore(Base):
    __tablename__ = "quiz_scores"

    id = Column(Integer, primary_key=True, index=True)

    quiz_id = Column(Integer, nullable=False)

    student_id = Column(Integer, nullable=False)

    attempt_number = Column(Integer, default=1)

    total_marks = Column(Float, default=0)

    obtained_marks = Column(Float, default=0)

    percentage = Column(Float, default=0)

    correct_answers = Column(Integer, default=0)

    wrong_answers = Column(Integer, default=0)

    skipped_answers = Column(Integer, default=0)

    status = Column(String, default="completed")

    started_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    submitted_at = Column(
        DateTime,
        default=datetime.utcnow
    )