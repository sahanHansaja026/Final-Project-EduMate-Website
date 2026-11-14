from sqlalchemy import Column, Integer, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class AssignmentViewAccess(Base):
    __tablename__ = "assignment_view_accesses"

    id = Column(Integer, primary_key=True, index=True)
    assignment_id = Column(Integer, ForeignKey("assignments.assignment_id"))
    user_id = Column(Integer, ForeignKey("users.user_id"))
    granted_at = Column(DateTime, default=datetime.utcnow)

    assignment = relationship("Assignment", back_populates="view_access")