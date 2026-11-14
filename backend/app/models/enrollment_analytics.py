from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey
from datetime import datetime
from sqlalchemy.orm import relationship
from database import Base

class EnrollmentAnalytics(Base):
    __tablename__ = "enrollment_analytics"

    id = Column(Integer, primary_key=True, index=True)
    module_id = Column(Integer, ForeignKey("modules.module_id"))
    total_users = Column(Integer, default=0)
    total_enrollments = Column(Integer, default=0)
    completion_rate = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)

    module = relationship("Module", back_populates="enrollment_analytics")