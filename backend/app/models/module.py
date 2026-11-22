from sqlalchemy import Column, Integer, String, Text, Enum, LargeBinary, ForeignKey, JSON
from sqlalchemy.dialects.postgresql import ARRAY as PG_ARRAY
from app.core.database import Base
import enum

class VisibilityEnum(str, enum.Enum):
    public = "public"
    private = "private"

class Module(Base):
    __tablename__ = "modules"

    module_id = Column(Integer, primary_key=True, index=True)  # renamed id
    user_id = Column(Integer, nullable=False)  # new field
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    cover_image = Column(LargeBinary, nullable=True)  # image bytes
    cover_image_name = Column(String(255), nullable=True)  # original filename
    skills = Column(PG_ARRAY(String).with_variant(JSON, "sqlite"), default=[])
    visibility = Column(Enum(VisibilityEnum), default=VisibilityEnum.public)
