from sqlalchemy import Column, Integer, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base

class AssignmentModuleGrade(Base):
    __tablename__ = "assignment_module_grades"

    id = Column(Integer, primary_key=True, index=True)
    assignment_id = Column(Integer, ForeignKey("assignments.id"))
    module_id = Column(Integer, ForeignKey("modules.module_id"))
    grade = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)

    assignment = relationship("Assignment")
    module = relationship("Module")