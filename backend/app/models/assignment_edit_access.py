from sqlalchemy import Column, Integer, Boolean, ForeignKey, DateTime
from datetime import datetime
from sqlalchemy.orm import relationship
from sqlalchemy.orm import relationship
from database import Base

class AssignmentEditAccess(Base):
    __tablename__ = "assignment_edit_accesses"

    id = Column(Integer, primary_key=True, index=True)
    assignment_id = Column(Integer, ForeignKey("assignments.assignment_id"))
    user_id = Column(Integer, ForeignKey("users.user_id"))
    granted_at = Column(DateTime, default=datetime.utcnow)

    assignment = relationship("Assignment", back_populates="edit_access")