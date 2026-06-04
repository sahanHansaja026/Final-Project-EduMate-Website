from pydantic import BaseModel
from typing import List, Optional
from models.channel import ChannelVisibilityEnum


class ChannelResponse(BaseModel):
    channel_id: int
    user_id: int

    channel_name: str
    description: Optional[str]

    institute_legal_name: str
    institute_owner_full_name: str
    physical_corporate_address: Optional[str]

    co_hosts_and_faculty_members: List[str]

    visibility: ChannelVisibilityEnum

    official_website_link: Optional[str]
    facebook_portal_link: Optional[str]

    cover_image: Optional[str]
    logo_image: Optional[str]

    class Config:
        from_attributes = True