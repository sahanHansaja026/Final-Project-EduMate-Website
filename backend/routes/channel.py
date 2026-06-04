import os
import json
import shutil
from typing import List

from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models.channel import Channel, ChannelVisibilityEnum
from schemas.channel import ChannelResponse

router = APIRouter(prefix="/channels", tags=["Channels"])

UPLOAD_DIR = "uploads/channel"
os.makedirs(UPLOAD_DIR, exist_ok=True)


# -------------------------
# CREATE CHANNEL
# -------------------------
@router.post("/", response_model=ChannelResponse)
async def create_channel(
    user_id: int = Form(...),
    channel_name: str = Form(...),
    description: str = Form(None),

    institute_legal_name: str = Form(...),
    institute_owner_full_name: str = Form(...),
    physical_corporate_address: str = Form(None),

    co_hosts_and_faculty_members: str = Form("[]"),

    visibility: ChannelVisibilityEnum = Form(...),

    official_website_link: str = Form(None),
    facebook_portal_link: str = Form(None),

    cover_image: UploadFile = File(None),
    logo_image: UploadFile = File(None),

    db: Session = Depends(get_db),
):
    faculty_list = json.loads(co_hosts_and_faculty_members)

    cover_path = None
    logo_path = None

    # Save cover image
    if cover_image:
        cover_path = os.path.join(
            UPLOAD_DIR,
            f"cover_{cover_image.filename}"
        )
        with open(cover_path, "wb") as buffer:
            shutil.copyfileobj(cover_image.file, buffer)

    # Save logo image
    if logo_image:
        logo_path = os.path.join(
            UPLOAD_DIR,
            f"logo_{logo_image.filename}"
        )
        with open(logo_path, "wb") as buffer:
            shutil.copyfileobj(logo_image.file, buffer)

    channel = Channel(
        user_id=user_id,
        channel_name=channel_name,
        description=description,
        institute_legal_name=institute_legal_name,
        institute_owner_full_name=institute_owner_full_name,
        physical_corporate_address=physical_corporate_address,
        co_hosts_and_faculty_members=faculty_list,
        visibility=visibility,
        official_website_link=official_website_link,
        facebook_portal_link=facebook_portal_link,
        cover_image=cover_path,
        logo_image=logo_path
    )

    db.add(channel)
    db.commit()
    db.refresh(channel)

    return ChannelResponse.from_orm(channel)


# -------------------------
# GET BY USER
# -------------------------
@router.get("/user/{user_id}", response_model=List[ChannelResponse])
def get_channels_by_user(user_id: int, db: Session = Depends(get_db)):
    return db.query(Channel).filter(Channel.user_id == user_id).all()


# -------------------------
# GET PUBLIC
# -------------------------
@router.get("/public", response_model=List[ChannelResponse])
def get_public_channels(db: Session = Depends(get_db)):
    return db.query(Channel).filter(
        Channel.visibility == ChannelVisibilityEnum.public
    ).all()


# -------------------------
# GET BY ID
# -------------------------
@router.get("/{channel_id}", response_model=ChannelResponse)
def get_channel(channel_id: int, db: Session = Depends(get_db)):
    channel = db.query(Channel).filter(
        Channel.channel_id == channel_id
    ).first()

    if not channel:
        raise HTTPException(status_code=404, detail="Channel not found")

    return channel


# -------------------------
# UPDATE CHANNEL
# -------------------------
@router.put("/{channel_id}", response_model=ChannelResponse)
async def update_channel(
    channel_id: int,

    channel_name: str = Form(None),
    description: str = Form(None),

    institute_legal_name: str = Form(None),
    institute_owner_full_name: str = Form(None),
    physical_corporate_address: str = Form(None),

    co_hosts_and_faculty_members: str = Form(None),

    visibility: ChannelVisibilityEnum = Form(None),

    official_website_link: str = Form(None),
    facebook_portal_link: str = Form(None),

    cover_image: UploadFile = File(None),
    logo_image: UploadFile = File(None),

    db: Session = Depends(get_db),
):
    channel = db.query(Channel).filter(
        Channel.channel_id == channel_id
    ).first()

    if not channel:
        raise HTTPException(status_code=404, detail="Channel not found")

    if channel_name is not None:
        channel.channel_name = channel_name

    if description is not None:
        channel.description = description

    if institute_legal_name is not None:
        channel.institute_legal_name = institute_legal_name

    if institute_owner_full_name is not None:
        channel.institute_owner_full_name = institute_owner_full_name

    if physical_corporate_address is not None:
        channel.physical_corporate_address = physical_corporate_address

    if co_hosts_and_faculty_members is not None:
        channel.co_hosts_and_faculty_members = json.loads(co_hosts_and_faculty_members)

    if visibility is not None:
        channel.visibility = visibility

    if official_website_link is not None:
        channel.official_website_link = official_website_link

    if facebook_portal_link is not None:
        channel.facebook_portal_link = facebook_portal_link

    # update cover image
    if cover_image:
        cover_path = os.path.join(
            UPLOAD_DIR,
            f"cover_{cover_image.filename}"
        )
        with open(cover_path, "wb") as buffer:
            shutil.copyfileobj(cover_image.file, buffer)
        channel.cover_image = cover_path

    # update logo image
    if logo_image:
        logo_path = os.path.join(
            UPLOAD_DIR,
            f"logo_{logo_image.filename}"
        )
        with open(logo_path, "wb") as buffer:
            shutil.copyfileobj(logo_image.file, buffer)
        channel.logo_image = logo_path

    db.commit()
    db.refresh(channel)

    return channel

# get all 
@router.get("/", response_model=List[ChannelResponse])
def get_all_channels(db: Session = Depends(get_db)):
    channels = db.query(Channel).all()
    return channels

