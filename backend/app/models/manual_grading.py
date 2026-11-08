from sqlalchemy import Column, Integer, Float, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class ManualGrading(Base):
    __tablename__ = "manual_gradings"

    id = Column(Integer, primary_key=True, index=True)
    assignment_id = Column(Integer, ForeignKey("assignments.assignment_id"))
    student_id = Column(Integer, ForeignKey("users.user_id"))
    grade = Column(Float)
    feedback = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    assignment = relationship("Assignment", back_populates="manual_gradings")
    student = relationship("User", back_populates="manual_gradings")