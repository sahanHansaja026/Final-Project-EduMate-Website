# models/chaneel_modules.py

from sqlalchemy import Column, Integer, String, Text, Enum
from sqlalchemy.dialects.postgresql import ARRAY as PG_ARRAY
from database import Base
import enum


class VisibilityEnum(str, enum.Enum):
    public = "public"
    private = "private"


class ChannelModule(Base):
    __tablename__ = "channel_modules"

    module_id = Column(Integer, primary_key=True, index=True)

    channel_id = Column(Integer, nullable=False)
    user_id = Column(Integer, nullable=False)

    co_host_email = Column(Text, nullable=True)

    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)

    # store filename only
    cover_image = Column(String(255), nullable=True)
    cover_image_name = Column(String(255), nullable=True)

    skills = Column(PG_ARRAY(String), default=list)

    visibility = Column(
        Enum(VisibilityEnum),
        default=VisibilityEnum.public,
        nullable=False
    )