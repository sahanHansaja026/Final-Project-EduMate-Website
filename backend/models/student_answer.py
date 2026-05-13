from sqlalchemy import (
    Column,
    Integer,
    Text,
    Boolean,
    Float
)

from database import Base


class StudentAnswer(Base):
    __tablename__ = "student_answers"

    id = Column(Integer, primary_key=True, index=True)

    quiz_id = Column(Integer, nullable=False)

    question_id = Column(Integer, nullable=False)

    student_id = Column(Integer, nullable=False)

    selected_option_id = Column(Integer, nullable=True)

    answer_text = Column(Text, nullable=True)

    is_correct = Column(Boolean, default=False)

    obtained_marks = Column(Float, default=0)