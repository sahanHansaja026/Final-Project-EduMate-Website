from sqlalchemy import Column, Integer, String, Text, Enum
from sqlalchemy.dialects.postgresql import ARRAY as PG_ARRAY
from database import Base
import enum


class ChannelVisibilityEnum(str, enum.Enum):
    public = "public"
    private = "private"


class Channel(Base):
    __tablename__ = "channels"

    channel_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)

    channel_name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)

    institute_legal_name = Column(String(255), nullable=False)
    institute_owner_full_name = Column(String(255), nullable=False)
    physical_corporate_address = Column(Text, nullable=True)

    co_hosts_and_faculty_members = Column(PG_ARRAY(String), default=[])

    visibility = Column(
        Enum(ChannelVisibilityEnum),
        default=ChannelVisibilityEnum.public,
        nullable=False
    )

    official_website_link = Column(String(500), nullable=True)
    facebook_portal_link = Column(String(500), nullable=True)

    cover_image = Column(String(500), nullable=True)
    logo_image = Column(String(500), nullable=True)