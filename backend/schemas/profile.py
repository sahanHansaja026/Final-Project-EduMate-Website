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


class ProfileCreate(BaseModel):
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


class ProfileResponse(ProfileCreate):
    id: int
    photo: Optional[str] = None
    coverPhoto: Optional[str] = None

    class Config:
        orm_mode = True
