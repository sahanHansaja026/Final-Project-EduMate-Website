from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from database import Base

class Quiz(Base):
    __tablename__ = "quizzes"

    id = Column(Integer, primary_key=True, index=True)

    module_id = Column(Integer, nullable=False)

    title = Column(String, nullable=False)
    description = Column(String, nullable=True)

    attempts = Column(String, default="unlimited")  # "1", "2", or "unlimited"

    open_date = Column(DateTime, nullable=True)
    close_date = Column(DateTime, nullable=True)

    is_graded = Column(Boolean, default=True)
    shuffle_questions = Column(Boolean, default=False)