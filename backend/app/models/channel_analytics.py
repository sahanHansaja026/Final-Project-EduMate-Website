from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class ChannelAnalytics(Base):
    __tablename__ = "channel_analytics"

    id = Column(Integer, primary_key=True, index=True)
    channel_id = Column(Integer, ForeignKey("channels.channel_id"))
    total_students = Column(Integer, default=0)
    total_modules = Column(Integer, default=0)
    total_enrollments = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)

    channel = relationship("Channel", back_populates="analytics")