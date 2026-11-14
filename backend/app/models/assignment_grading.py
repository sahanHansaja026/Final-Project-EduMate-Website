from sqlalchemy import Column, Integer, Float, ForeignKey, DateTime, Text
from datetime import datetime
from sqlalchemy.orm import relationship
from database import Base

class AssignmentGrading(Base):
    __tablename__ = "assignment_gradings"

    id = Column(Integer, primary_key=True, index=True)
    assignment_id = Column(Integer, ForeignKey("assignments.assignment_id"))
    student_id = Column(Integer, ForeignKey("users.user_id"))
    grade = Column(Float)
    feedback = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    assignment = relationship("Assignment", back_populates="gradings")
    student = relationship("User", back_populates="assignment_gradings")