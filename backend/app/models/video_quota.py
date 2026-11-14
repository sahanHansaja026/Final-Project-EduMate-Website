from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class VideoQuota(Base):
    __tablename__ = "video_quotas"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    plan_type = Column(String(50))
    videos_watched = Column(Integer, default=0)
    videos_limit = Column(Integer, default=3)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="video_quotas")