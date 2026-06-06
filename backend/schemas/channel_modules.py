# schemas/channel_modules.py

from pydantic import BaseModel, Field
from typing import List, Optional
from models.chaneel_modules import VisibilityEnum


class ChannelModuleCreate(BaseModel):
    user_id: int
    channel_id: int
    name: str
    description: Optional[str] = None
    co_host_email: Optional[str] = None
    skills: List[str] = Field(default_factory=list)
    visibility: VisibilityEnum


class ChannelModuleResponse(BaseModel):
    module_id: int
    user_id: int
    channel_id: int
    name: str
    description: Optional[str] = None

    co_host_email: Optional[str] = None

    cover_image: Optional[str] = None
    cover_image_name: Optional[str] = None

    skills: List[str] = Field(default_factory=list)
    visibility: VisibilityEnum

    class Config:
        from_attributes = True

    @classmethod
    def from_orm(cls, obj):
        return cls(
            module_id=obj.module_id,
            user_id=obj.user_id,
            channel_id=obj.channel_id,
            name=obj.name,
            description=obj.description,
            co_host_email=obj.co_host_email,
            cover_image=obj.cover_image,
            cover_image_name=obj.cover_image_name,
            skills=obj.skills or [],
            visibility=obj.visibility
        )