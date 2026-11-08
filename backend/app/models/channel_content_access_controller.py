from sqlalchemy import Column, Integer, ForeignKey, DateTime
from datetime import datetime
from sqlalchemy.orm import relationship
from sqlalchemy.orm import relationship
from database import Base

class ChannelContentAccessController(Base):
    __tablename__ = "channel_content_access_controller"

    id = Column(Integer, primary_key=True, index=True)
    channel_id = Column(Integer, ForeignKey("channels.channel_id"))
    content_id = Column(Integer, ForeignKey("content.content_id"))
    user_id = Column(Integer, ForeignKey("users.user_id"))
    granted_at = Column(DateTime, default=datetime.utcnow)

    channel = relationship("Channel", back_populates="content_access_controllers")
    content = relationship("Content", back_populates="channel_access_controllers")
    user = relationship("User", back_populates="content_access_controllers")