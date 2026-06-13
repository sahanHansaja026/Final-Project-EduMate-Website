import os
import json
from typing import List
from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models.channel import Channel, ChannelVisibilityEnum
from schemas.channel import ChannelResponse
from services.s3_service import upload_file, delete_file

router = APIRouter(prefix="/channels", tags=["Channels"])


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
    try:
        faculty_list = json.loads(co_hosts_and_faculty_members)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid faculty members JSON format")

    cover_path = None
    logo_path = None

    # Stream directly to S3 if files are provided
    if cover_image:
        try:
            cover_path = upload_file(cover_image, folder="channels/covers")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Cover image upload failed: {str(e)}")

    if logo_image:
        try:
            logo_path = upload_file(logo_image, folder="channels/logos")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Logo image upload failed: {str(e)}")

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

    return channel


# -------------------------
# GET ALL CHANNELS
# -------------------------
@router.get("/", response_model=List[ChannelResponse])
def get_all_channels(db: Session = Depends(get_db)):
    return db.query(Channel).all()


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

    # Update fields
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
        try:
            channel.co_hosts_and_faculty_members = json.loads(co_hosts_and_faculty_members)
        except Exception:
            raise HTTPException(status_code=400, detail="Invalid faculty members JSON format")

    if visibility is not None:
        channel.visibility = visibility

    if official_website_link is not None:
        channel.official_website_link = official_website_link

    if facebook_portal_link is not None:
        channel.facebook_portal_link = facebook_portal_link

    # Handle Cover Image updates via S3
    if cover_image and cover_image.filename:
        if channel.cover_image and "amazonaws.com" in channel.cover_image:
            try:
                delete_file(channel.cover_image)
            except Exception as e:
                print(f"Failed to delete old cover: {e}")

        try:
            channel.cover_image = upload_file(cover_image, folder="channels/covers")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to upload new cover image: {str(e)}")

    # Handle Logo Image updates via S3
    if logo_image and logo_image.filename:
        if channel.logo_image and "amazonaws.com" in channel.logo_image:
            try:
                delete_file(channel.logo_image)
            except Exception as e:
                print(f"Failed to delete old logo: {e}")

        try:
            channel.logo_image = upload_file(logo_image, folder="channels/logos")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to upload new logo image: {str(e)}")

    db.commit()
    db.refresh(channel)

    return channel


# -------------------------
# AUTHORIZATION CHECK
# -------------------------
@router.get("/{channel_id}/authorize")
def authorize_channel_access(
    channel_id: int,
    current_user_id: int,
    current_email: str,
    db: Session = Depends(get_db)
):
    channel = db.query(Channel).filter(Channel.channel_id == channel_id).first()

    if not channel:
        raise HTTPException(status_code=404, detail="Channel not found")

    # Owner check
    if channel.user_id == current_user_id:
        return {
            "authorized": True,
            "role": "owner"
        }

    # Co-host check
    co_hosts = channel.co_hosts_and_faculty_members or []

    for member in co_hosts:
        if (
            isinstance(member, dict)
            and member.get("email", "").lower() == current_email.lower()
        ):
            return {
                "authorized": True,
                "role": "co_host"
            }

    return {
        "authorized": False,
        "role": None
    }


# -------------------------
# DELETE CHANNEL
# -------------------------
@router.delete("/{channel_id}")
def delete_channel(channel_id: int, db: Session = Depends(get_db)):
    channel = db.query(Channel).filter(Channel.channel_id == channel_id).first()

    if not channel:
        raise HTTPException(status_code=404, detail="Channel not found")

    # Clean assets from S3 bucket before structural database drops
    if channel.cover_image and "amazonaws.com" in channel.cover_image:
        delete_file(channel.cover_image)

    if channel.logo_image and "amazonaws.com" in channel.logo_image:
        delete_file(channel.logo_image)

    db.delete(channel)
    db.commit()

    return {"message": "Channel and its linked cloud assets deleted successfully"}