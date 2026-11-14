from sqlalchemy import Column, Integer, String, Text, Date, DateTime
from database import Base
from datetime import datetime


class Video(Base):
    __tablename__ = "videos"

    id = Column(Integer, primary_key=True, index=True)

    module_id = Column(Integer, nullable=False)

    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)

    source_type = Column(String(50), nullable=False)
    # YouTube | Vimeo | Upload

    video_url = Column(Text, nullable=True)
    # external URL OR uploaded video path

    thumbnail_url = Column(Text, nullable=True)

    open_date = Column(Date, nullable=True)
    close_date = Column(Date, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)