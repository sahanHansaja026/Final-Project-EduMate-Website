from pydantic import BaseModel
from typing import List, Optional
from models.module import VisibilityEnum
import base64

class ModuleCreate(BaseModel):
    user_id: int
    name: str
    description: Optional[str] = None
    skills: List[str] = []
    visibility: VisibilityEnum

class ModuleResponse(BaseModel):
    module_id: int
    user_id: int
    name: str
    description: Optional[str]
    cover_image: Optional[str]  # base64 string
    cover_image_name: Optional[str]
    skills: List[str]
    visibility: VisibilityEnum

    class Config:
        from_attributes = True

    @classmethod
    def from_orm(cls, obj):
        cover_base64 = None
        if obj.cover_image:
            cover_base64 = base64.b64encode(obj.cover_image).decode("utf-8")
        return cls(
            module_id=obj.module_id,
            user_id=obj.user_id,
            name=obj.name,
            description=obj.description,
            cover_image=cover_base64,
            cover_image_name=obj.cover_image_name,
            skills=obj.skills,
            visibility=obj.visibility
        )
