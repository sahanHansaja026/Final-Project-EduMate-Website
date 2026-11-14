from sqlalchemy import Column, Integer, Float, ForeignKey, DateTime
from datetime import datetime
from sqlalchemy.orm import relationship
from database import Base

class Grade(Base):
    __tablename__ = "grades"

    id = Column(Integer, primary_key=True, index=True)
    assignment_id = Column(Integer, ForeignKey("assignments.assignment_id"))
    student_id = Column(Integer, ForeignKey("users.user_id"))
    score = Column(Float)
    max_score = Column(Float, default=100.0)
    created_at = Column(DateTime, default=datetime.utcnow)

    assignment = relationship("Assignment", back_populates="grades")
    student = relationship("User", back_populates="grades")