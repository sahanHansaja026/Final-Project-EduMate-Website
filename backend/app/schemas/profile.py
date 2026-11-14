from pydantic import BaseModel, EmailStr
from typing import Optional
from enum import Enum


class PushNotifications(str, Enum):
    everything = "everything"
    email = "email"
    none = "none"


class Notifications(BaseModel):
    comments: bool
    candidates: bool
    offers: bool
    push: PushNotifications


class ProfileBase(BaseModel):
    username: str
    about: Optional[str] = None

    firstName: str
    lastName: str
    email: EmailStr

    country: str
    streetAddress: str
    city: str
    region: str
    postalCode: str

    notifications: Notifications


class ProfileCreate(ProfileBase):
    pass  # Used for input creation/updating via form


class ProfileResponse(ProfileBase):
    id: int
    photo: Optional[str] = None  # base64 string
    coverPhoto: Optional[str] = None  # base64 string

    class Config:
        from_attributes = True
