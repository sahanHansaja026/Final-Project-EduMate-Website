"""Profile management endpoints."""

from typing import Optional

from fastapi import APIRouter, Depends, File, Form, Path, Query, UploadFile
from pydantic import EmailStr
from sqlalchemy.orm import Session

from app.controllers import profile_controller
from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.schemas.profile import ProfileResponse, PushNotifications


router = APIRouter(prefix="/profiles", tags=["Profiles"])


@router.get("/", response_model=ProfileResponse, tags=["Profiles"])
def get_profile(
    email: EmailStr = Query(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Retrieve a user profile by email, enforcing ownership."""
    return profile_controller.get_profile(email, current_user, db)


@router.post("/", response_model=ProfileResponse, status_code=201, tags=["Profiles"])
async def create_or_update_profile(
    username: str = Form(...),
    about: Optional[str] = Form(None),
    firstName: str = Form(...),
    lastName: str = Form(...),
    email: EmailStr = Form(...),
    country: str = Form(...),
    streetAddress: str = Form(...),
    city: str = Form(...),
    region: str = Form(...),
    postalCode: str = Form(...),
    comments: bool = Form(...),
    candidates: bool = Form(...),
    offers: bool = Form(...),
    push: PushNotifications = Form(...),
    photo: Optional[UploadFile] = File(None),
    coverPhoto: Optional[UploadFile] = File(None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Create or update a user profile (multipart form + optional photo uploads)."""
    return await profile_controller.create_or_update_profile(
        db,
        current_user=current_user,
        username=username,
        about=about,
        first_name=firstName,
        last_name=lastName,
        email=email,
        country=country,
        street_address=streetAddress,
        city=city,
        region=region,
        postal_code=postalCode,
        notify_comments=comments,
        notify_candidates=candidates,
        notify_offers=offers,
        push=push,
        photo=photo,
        coverPhoto=coverPhoto,
    )


@router.put("/{profile_id}", response_model=ProfileResponse, tags=["Profiles"])
async def update_profile_by_id(
    profile_id: int = Path(...),
    username: str = Form(...),
    about: Optional[str] = Form(None),
    firstName: str = Form(...),
    lastName: str = Form(...),
    email: EmailStr = Form(...),
    country: str = Form(...),
    streetAddress: str = Form(...),
    city: str = Form(...),
    region: str = Form(...),
    postalCode: str = Form(...),
    comments: bool = Form(...),
    candidates: bool = Form(...),
    offers: bool = Form(...),
    push: PushNotifications = Form(...),
    photo: Optional[UploadFile] = File(None),
    coverPhoto: Optional[UploadFile] = File(None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Update a user profile by id (multipart form + optional photo uploads)."""
    return await profile_controller.create_or_update_profile(
        db,
        current_user=current_user,
        username=username,
        about=about,
        first_name=firstName,
        last_name=lastName,
        email=email,
        country=country,
        street_address=streetAddress,
        city=city,
        region=region,
        postal_code=postalCode,
        notify_comments=comments,
        notify_candidates=candidates,
        notify_offers=offers,
        push=push,
        photo=photo,
        coverPhoto=coverPhoto,
        profile_id=profile_id,
    )


@router.delete("/{profile_id}", tags=["Profiles"])
def delete_profile(
    profile_id: int = Path(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Delete a user profile by id, enforcing ownership."""
    return profile_controller.delete_profile(profile_id, current_user, db)


@router.get("/photo", tags=["Profiles"])
def get_profile_photo(
    email: EmailStr = Query(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Serve the raw profile photo of a user, enforcing ownership."""
    return profile_controller.get_profile_photo(email, current_user, db)


@router.get("/by-email", tags=["Profiles"])
def get_user_name_by_email(
    email: EmailStr = Query(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Retrieve the display names of a user by email, enforcing ownership."""
    return profile_controller.get_user_name_by_email(email, current_user, db)
