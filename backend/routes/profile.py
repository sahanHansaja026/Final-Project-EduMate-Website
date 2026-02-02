from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
import base64
from fastapi.responses import Response
from models.profile import Profile
from schemas.profile import PushNotifications, ProfileResponse, Notifications
from database import get_db

router = APIRouter(prefix="/profiles", tags=["Profiles"])

@router.get("/", response_model=ProfileResponse)
def get_profile(email: str = Query(...), db: Session = Depends(get_db)):
    profile = db.query(Profile).filter(Profile.email == email).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")

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

@router.post("/", response_model=ProfileResponse, status_code=201)
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

    db: Session = Depends(get_db),
):
    try:
        # Check if profile already exists
        profile = db.query(Profile).filter(Profile.email == email).first()

        # Read uploaded files
        photo_bytes = await photo.read() if photo else None
        cover_bytes = await coverPhoto.read() if coverPhoto else None

        if profile:
            # Update existing profile
            profile.username = username
            profile.about = about
            profile.first_name = firstName
            profile.last_name = lastName
            profile.country = country
            profile.street_address = streetAddress
            profile.city = city
            profile.region = region
            profile.postal_code = postalCode
            profile.notify_comments = comments
            profile.notify_candidates = candidates
            profile.notify_offers = offers
            profile.push_notifications = push
            if photo_bytes:
                profile.photo = photo_bytes
            if cover_bytes:
                profile.cover_photo = cover_bytes

            db.commit()
            db.refresh(profile)
        else:
            # Create new profile
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
        raise HTTPException(status_code=500, detail=f"Error saving profile: {e}")


@router.get("/photo")
def get_profile_photo(
    email: str = Query(...),
    db: Session = Depends(get_db)
):
    profile = db.query(Profile).filter(Profile.email == email).first()

    if not profile or not profile.photo:
        raise HTTPException(status_code=404, detail="Profile photo not found")

    return Response(
        content=profile.photo,
        media_type="image/jpeg"  # use image/png if needed
    )
