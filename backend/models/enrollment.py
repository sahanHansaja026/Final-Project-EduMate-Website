from sqlalchemy import Column, Integer, Boolean, DateTime, ForeignKey
from datetime import datetime
from database import Base

class Enrollment(Base):
    __tablename__ = "enrollments"

    enrollment_id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    module_id = Column(Integer, ForeignKey("modules.module_id"), nullable=False)

    enrolled_at = Column(DateTime, default=datetime.utcnow)
    completed = Column(Boolean, default=False)