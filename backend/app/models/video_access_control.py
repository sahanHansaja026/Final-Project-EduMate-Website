from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base

class VideoAccessControl(Base):
    __tablename__ = "video_access_controls"

    id = Column(Integer, primary_key=True, index=True)
    video_id = Column(Integer, ForeignKey("videos.id"))
    user_id = Column(Integer, ForeignKey("users.user_id"))
    plan_type = Column(String(50))
    granted_at = Column(DateTime, default=datetime.utcnow)

    video = relationship("Video")
    user = relationship("User")