# routes/channel_modules.py

from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException
from sqlalchemy.orm import Session
import json
import os
import uuid

from models.chaneel_modules import ChannelModule, VisibilityEnum
from schemas.channel_modules import ChannelModuleResponse
from database import get_db

router = APIRouter(prefix="/channel-modules", tags=["Channel Modules"])


# =========================
# UPLOAD CONFIG
# =========================
UPLOAD_DIR = "uploads/channel_modules"
os.makedirs(UPLOAD_DIR, exist_ok=True)


# =========================
# CREATE MODULE
# =========================
@router.post("/", response_model=ChannelModuleResponse)
async def create_channel_module(
    user_id: int = Form(...),
    channel_id: int = Form(...),
    name: str = Form(...),
    description: str = Form(None),
    co_host_email: str = Form(None),
    skills: str = Form("[]"),
    visibility: VisibilityEnum = Form(...),
    cover_image: UploadFile = File(None),
    db: Session = Depends(get_db),
):

    # parse skills
    try:
        skills_list = json.loads(skills)
        if not isinstance(skills_list, list):
            raise ValueError()
    except:
        raise HTTPException(status_code=400, detail="Invalid skills format")

    # save image file
    filename = None
    if cover_image:
        ext = cover_image.filename.split(".")[-1]
        filename = f"{uuid.uuid4()}.{ext}"
        file_path = os.path.join(UPLOAD_DIR, filename)

        with open(file_path, "wb") as f:
            f.write(await cover_image.read())

    # create DB record
    new_module = ChannelModule(
        user_id=user_id,
        channel_id=channel_id,
        name=name,
        description=description,
        co_host_email=co_host_email,
        skills=skills_list,
        visibility=visibility,
        cover_image=filename,
        cover_image_name=cover_image.filename if cover_image else None,
    )

    db.add(new_module)
    db.commit()
    db.refresh(new_module)

    return ChannelModuleResponse.from_orm(new_module)


# =========================
# GET BY CHANNEL ID
# =========================
@router.get("/channel/{channel_id}", response_model=list[ChannelModuleResponse])
def get_modules_by_channel(
    channel_id: int,
    db: Session = Depends(get_db)
):
    modules = (
        db.query(ChannelModule)
        .filter(ChannelModule.channel_id == channel_id)
        .order_by(ChannelModule.module_id.desc())
        .all()
    )

    return [ChannelModuleResponse.from_orm(m) for m in modules]