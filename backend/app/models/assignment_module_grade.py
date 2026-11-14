from sqlalchemy import Column, Integer, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class AssignmentModuleGrade(Base):
    __tablename__ = "assignment_module_grades"

    id = Column(Integer, primary_key=True, index=True)
    assignment_id = Column(Integer, ForeignKey("assignments.assignment_id"))
    module_id = Column(Integer, ForeignKey("modules.module_id"))
    grade = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)

    assignment = relationship("Assignment", back_populates="module_grades")
    module = relationship("Module", back_populates="assignment_grades")