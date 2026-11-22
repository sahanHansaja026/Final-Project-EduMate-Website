"""User management endpoints (authentication + profile management)."""

from typing import Optional

from fastapi import APIRouter, Depends, File, Form, Path, Query, UploadFile
from sqlalchemy.orm import Session

from app.controllers import user_controller
from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.schemas.profile import ProfileResponse, PushNotifications
from app.schemas.user import LoginSchema, SignupSchema, TokenSchema

router = APIRouter()


# ---------------- AUTHENTICATION / USER ACCOUNT ----------------
@router.post("/auth/signup", status_code=201, tags=["Auth"])
def signup(data: SignupSchema, db: Session = Depends(get_db)):
    """Register a new user and provision the free subscription plan."""
    return user_controller.signup(data, db)


@router.post("/auth/login", response_model=TokenSchema, tags=["Auth"])
def login(data: LoginSchema, db: Session = Depends(get_db)):
    """Authenticate a user and return access/refresh tokens."""
    return user_controller.login(data, db)


@router.post("/auth/logout", tags=["Auth"])
def logout(refresh_token: str, db: Session = Depends(get_db)):
    """Invalidate the refresh token of a logged out session."""
    return user_controller.logout(refresh_token, db)


# ---------------- USER PROFILE MANAGEMENT ----------------
@router.get("/profiles/", response_model=ProfileResponse, tags=["Profiles"])
def get_profile(
    email: str = Query(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Retrieve a user profile by email, enforcing ownership."""
    return user_controller.get_profile(email, current_user, db)


@router.post("/profiles/", response_model=ProfileResponse, status_code=201, tags=["Profiles"])
async def create_or_update_profile(
    username: str = Form(...),
    about: Optional[str] = Form(None),
    firstName: str = Form(...),
    lastName: str = Form(...),
    email: str = Form(...),
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
    return await user_controller.create_or_update_profile(
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


@router.put("/profiles/{profile_id}", response_model=ProfileResponse, tags=["Profiles"])
async def update_profile_by_id(
    profile_id: int = Path(...),
    username: str = Form(...),
    about: Optional[str] = Form(None),
    firstName: str = Form(...),
    lastName: str = Form(...),
    email: str = Form(...),
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
    return await user_controller.create_or_update_profile(
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


@router.get("/profiles/photo", tags=["Profiles"])
def get_profile_photo(
    email: str = Query(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Serve the raw profile photo of a user, enforcing ownership."""
    return user_controller.get_profile_photo(email, current_user, db)


@router.get("/profiles/by-email", tags=["Profiles"])
def get_user_name_by_email(
    email: str = Query(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Retrieve the display names of a user by email, enforcing ownership."""
    return user_controller.get_user_name_by_email(email, current_user, db)
