from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class ScoreManagement(Base):
    __tablename__ = "score_management"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("users.user_id"))
    assignment_id = Column(Integer, ForeignKey("assignments.assignment_id"))
    score = Column(Float)
    max_score = Column(Float, default=100.0)
    created_at = Column(DateTime, default=datetime.utcnow)

    student = relationship("User", back_populates="score_management")
    assignment = relationship("Assignment", back_populates="score_management")