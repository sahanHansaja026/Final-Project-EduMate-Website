from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from datetime import datetime
from database import Base

class AssignmentSubmission(Base):
    __tablename__ = "assignment_submissions"

    id = Column(Integer, primary_key=True, index=True)

    assignment_id = Column(Integer, index=True)
    student_id = Column(Integer, index=True)

    file_path = Column(String, nullable=False)

    submitted_at = Column(DateTime, default=datetime.utcnow)

    feedback = Column(Text, nullable=True)
    marks = Column(Integer, nullable=True)