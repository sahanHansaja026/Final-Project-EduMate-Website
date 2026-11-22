from sqlalchemy import Column, Integer, Float, ForeignKey, DateTime
from datetime import datetime
from sqlalchemy.orm import relationship
from app.core.database import Base

class QuizAttemptController(Base):
    __tablename__ = "quiz_attempt_controllers"

    id = Column(Integer, primary_key=True, index=True)
    quiz_id = Column(Integer, ForeignKey("quizzes.id"))
    user_id = Column(Integer, ForeignKey("users.user_id"))
    score = Column(Float)
    max_score = Column(Float)
    attempted_at = Column(DateTime, default=datetime.utcnow)

    quiz = relationship("Quiz")
    user = relationship("User")