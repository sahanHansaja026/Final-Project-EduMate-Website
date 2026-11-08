from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

from database import Base


class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)

    quiz_id = Column(Integer, ForeignKey("quizzes.id"), nullable=False)

    question_number = Column(Integer, nullable=False)

    question_type = Column(String, nullable=False)

    question_text = Column(Text, nullable=False)

    marks = Column(Integer, default=1)

    explanation = Column(Text, nullable=True)

    difficulty = Column(String, default="medium")

    is_required = Column(Boolean, default=True)

    allow_negative_marking = Column(Boolean, default=False)

    negative_marks = Column(Integer, default=0)

    created_at = Column(DateTime, default=datetime.utcnow)

    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    # relationships
    options = relationship(
        "QuestionOption",
        back_populates="question",
        cascade="all, delete"
    )