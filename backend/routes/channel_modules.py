import json
from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException, Path
from sqlalchemy.orm import Session
from typing import List

from services.s3_service import delete_file, upload_file
from database import get_db
from models.profile import Profile
from models.chaneel_modules import ChannelModule, VisibilityEnum
from schemas.channel_modules import ChannelModuleResponse

# Import your working S3 helper functions


router = APIRouter(prefix="/channel-modules", tags=["Channel Modules"])


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

    # Stream file directly to S3 if it exists
    cover_image_url = None
    if cover_image:
        try:
            cover_image_url = upload_file(cover_image, folder="channel_modules")
        except Exception as e:
            raise HTTPException(
                status_code=500, 
                detail=f"Failed to upload cover image to S3: {str(e)}"
            )

    # create DB record
    new_module = ChannelModule(
        user_id=user_id,
        channel_id=channel_id,
        name=name,
        description=description,
        co_host_email=co_host_email,
        skills=skills_list,
        visibility=visibility,
        cover_image=cover_image_url,  # Stores the S3 HTTPS URL string
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

    # Update basic fields
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

    if skills is not None:
        try:
            skills_list = json.loads(skills)
            if not isinstance(skills_list, list):
                raise ValueError()
            module.skills = skills_list
        except:
            raise HTTPException(status_code=400, detail="Invalid skills format")

    # Cover image update (S3 Cloud Delete + Upload)
    if cover_image:
        # 1. Clear old image out of S3 bucket if it exists
        if module.cover_image:
            delete_file(module.cover_image)

        # 2. Upload incoming file asset directly to S3
        try:
            module.cover_image = upload_file(cover_image, folder="channel_modules")
            module.cover_image_name = cover_image.filename
        except Exception as e:
            raise HTTPException(
                status_code=500, 
                detail=f"Failed to upload new cover image to S3: {str(e)}"
            )

    db.commit()
    db.refresh(module)

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
    

# =========================
# ACCESS CHECK
# =========================
@router.get("/access/{module_id}/{user_id}")
def check_channel_module_access(
    module_id: int = Path(...),
    user_id: int = Path(...),
    db: Session = Depends(get_db),
):
    module = (
        db.query(ChannelModule)
        .filter(ChannelModule.module_id == module_id)
        .first()
    )

    if not module:
        raise HTTPException(status_code=404, detail="Channel module not found")

    is_owner = module.user_id == user_id

    is_cohost = False
    if module.co_host_email:
        co_host = (
            db.query(Profile)
            .filter(Profile.email == module.co_host_email)
            .first()
        )

        if co_host and co_host.id == user_id:
            is_cohost = True

    is_public = module.visibility == VisibilityEnum.public
    has_access = is_owner or is_cohost or is_public

    return {
        "module_id": module_id,
        "user_id": user_id,
        "is_owner": is_owner,
        "is_cohost": is_cohost,
        "is_public": is_public,
        "has_access": has_access
    }
    

# =========================
# DELETE MODULE
# =========================
@router.delete("/module/{module_id}")
def delete_channel_module(
    module_id: int,
    db: Session = Depends(get_db),
):
    module = (
        db.query(ChannelModule)
        .filter(ChannelModule.module_id == module_id)
        .first()
    )

    if not module:
        raise HTTPException(status_code=404, detail="Module not found")

    # Clean out the asset directly from S3 bucket before structural database drops
    if module.cover_image:
        delete_file(module.cover_image)

    db.delete(module)
    db.commit()

    return {
        "message": "Channel module deleted successfully"
    }