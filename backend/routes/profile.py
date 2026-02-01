from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
import base64

from models.profile import Profile
from schemas.profile import PushNotifications, ProfileResponse, Notifications
from database import get_db

router = APIRouter(prefix="/profiles", tags=["Profiles"])


@router.post("/", response_model=ProfileResponse, status_code=201)
async def create_profile(
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

    db: Session = Depends(get_db),
):
    try:
        # Read photo bytes
        photo_bytes = await photo.read() if photo else None
        cover_bytes = await coverPhoto.read() if coverPhoto else None

        profile = Profile(
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
            push_notifications=push,
            photo=photo_bytes,
            cover_photo=cover_bytes,
        )

        db.add(profile)
        db.commit()
        db.refresh(profile)

        # Convert photos to base64 for response
        photo_b64 = base64.b64encode(profile.photo).decode("utf-8") if profile.photo else None
        cover_b64 = base64.b64encode(profile.cover_photo).decode("utf-8") if profile.cover_photo else None

        return ProfileResponse(
            id=profile.id,
            username=profile.username,
            about=profile.about,
            firstName=profile.first_name,
            lastName=profile.last_name,
            email=profile.email,
            country=profile.country,
            streetAddress=profile.street_address,
            city=profile.city,
            region=profile.region,
            postalCode=profile.postal_code,
            notifications=Notifications(
                comments=profile.notify_comments,
                candidates=profile.notify_candidates,
                offers=profile.notify_offers,
                push=profile.push_notifications
            ),
            photo=photo_b64,
            coverPhoto=cover_b64
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error creating profile: {e}")
