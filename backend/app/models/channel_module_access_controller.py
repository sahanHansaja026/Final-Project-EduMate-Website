from sqlalchemy import Column, Integer, ForeignKey, DateTime
from datetime import datetime
from sqlalchemy.orm import relationship
from sqlalchemy.orm import relationship
from database import Base

class ChannelModuleAccessController(Base):
    __tablename__ = "channel_module_access_controller"

    id = Column(Integer, primary_key=True, index=True)
    channel_id = Column(Integer, ForeignKey("channels.channel_id"))
    module_id = Column(Integer, ForeignKey("modules.module_id"))
    user_id = Column(Integer, ForeignKey("users.user_id"))
    granted_at = Column(DateTime, default=datetime.utcnow)

    channel = relationship("Channel", back_populates="module_access_controllers")
    module = relationship("Module", back_populates="module_access_controllers")
    user = relationship("User", back_populates="module_access_controllers")