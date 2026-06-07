# routes/channel_modules.py

from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException
from sqlalchemy.orm import Session
import json
import os
import uuid
from models.profile import Profile
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



@router.get("/channel/{channel_id}")
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

    result = []

    for module in modules:

        co_host = None

        if module.co_host_email:
            co_host = (
                db.query(Profile)
                .filter(Profile.email == module.co_host_email)
                .first()
            )

        result.append({
            "module_id": module.module_id,
            "user_id": module.user_id,
            "channel_id": module.channel_id,
            "name": module.name,
            "description": module.description,
            "skills": module.skills,
            "visibility": module.visibility,
            "cover_image": module.cover_image,
            "cover_image_name": module.cover_image_name,

            "co_host": {
                "email": co_host.email if co_host else module.co_host_email,
                "firstName": co_host.first_name if co_host else None,
                "lastName": co_host.last_name if co_host else None,
            } if module.co_host_email else None
        })

    return result

# =========================
# GET MODULE BY MODULE ID
# =========================

@router.get("/module/{module_id}")
def get_module_by_id(
    module_id: int,
    db: Session = Depends(get_db)
):
    module = (
        db.query(ChannelModule)
        .filter(ChannelModule.module_id == module_id)
        .first()
    )

    if not module:
        raise HTTPException(
            status_code=404,
            detail="Module not found"
        )

    co_host = None

    if module.co_host_email:
        co_host = (
            db.query(Profile)
            .filter(Profile.email == module.co_host_email)
            .first()
        )

    return {
        "module_id": module.module_id,
        "user_id": module.user_id,
        "channel_id": module.channel_id,
        "name": module.name,
        "description": module.description,
        "skills": module.skills,
        "visibility": module.visibility,
        "cover_image": module.cover_image,
        "cover_image_name": module.cover_image_name,
        "co_host": {
            "email": co_host.email if co_host else module.co_host_email,
            "firstName": co_host.first_name if co_host else None,
            "lastName": co_host.last_name if co_host else None,
        } if module.co_host_email else None
    }
    

# =========================
# UPDATE MODULE
# =========================
@router.put("/module/{module_id}", response_model=ChannelModuleResponse)
async def update_channel_module(
    module_id: int,
    user_id: int = Form(None),
    channel_id: int = Form(None),
    name: str = Form(None),
    description: str = Form(None),
    co_host_email: str = Form(None),
    skills: str = Form(None),
    visibility: VisibilityEnum = Form(None),
    cover_image: UploadFile = File(None),
    db: Session = Depends(get_db),
):

    module = (
        db.query(ChannelModule)
        .filter(ChannelModule.module_id == module_id)
        .first()
    )

    if not module:
        raise HTTPException(status_code=404, detail="Module not found")

    # =========================
    # UPDATE ONLY PROVIDED FIELDS
    # =========================
    if user_id is not None:
        module.user_id = user_id

    if channel_id is not None:
        module.channel_id = channel_id

    if name is not None:
        module.name = name

    if description is not None:
        module.description = description

    if co_host_email is not None:
        module.co_host_email = co_host_email

    if visibility is not None:
        module.visibility = visibility

    # =========================
    # SKILLS PARSE
    # =========================
    if skills is not None:
        try:
            skills_list = json.loads(skills)
            if not isinstance(skills_list, list):
                raise ValueError()
            module.skills = skills_list
        except:
            raise HTTPException(status_code=400, detail="Invalid skills format")

    # =========================
    # COVER IMAGE UPDATE
    # =========================
    if cover_image:
        ext = cover_image.filename.split(".")[-1]
        filename = f"{uuid.uuid4()}.{ext}"
        file_path = os.path.join(UPLOAD_DIR, filename)

        with open(file_path, "wb") as f:
            f.write(await cover_image.read())

        module.cover_image = filename
        module.cover_image_name = cover_image.filename

    # =========================
    # SAVE TO DB
    # =========================
    db.commit()
    db.refresh(module)

    # =========================
    # RESPONSE
    # =========================
    return {
        "module_id": module.module_id,
        "user_id": module.user_id,
        "channel_id": module.channel_id,
        "name": module.name,
        "description": module.description,
        "skills": module.skills,
        "visibility": module.visibility,
        "cover_image": module.cover_image,
        "cover_image_name": module.cover_image_name,
        "co_host": {
            "email": module.co_host_email
        } if module.co_host_email else None
    }