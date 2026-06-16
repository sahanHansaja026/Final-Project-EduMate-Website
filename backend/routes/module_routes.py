from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from database import get_db

from models.module import Module
from models.chaneel_modules import ChannelModule
from models.user import User
from models.profile import Profile

router = APIRouter(prefix="/modules", tags=["Modules"])


# -----------------------------
# GET USER OWNER INFO
# -----------------------------
def get_owner_info(db: Session, user_id: int):
    user = db.query(User).filter(User.user_id == user_id).first()

    if not user:
        return None

    profile = db.query(Profile).filter(Profile.email == user.email).first()

    return {
        "email": user.email,
        "first_name": profile.first_name if profile else None,
        "last_name": profile.last_name if profile else None,
    }


# -----------------------------
# FORMAT MODULE
# -----------------------------
def format_module(db: Session, m: Module):
    return {
        "type": "module",
        "module_id": m.module_id,
        "user_id": m.user_id,
        "name": m.name,
        "description": m.description,
        "cover_image_name": m.cover_image_name,
        "skills": m.skills or [],
        "visibility": m.visibility.value if m.visibility else None,

        # 🔥 OWNER DETAILS ADDED
        "owner": get_owner_info(db, m.user_id),
    }


# -----------------------------
# FORMAT CHANNEL MODULE
# -----------------------------
def format_channel_module(db: Session, cm: ChannelModule):
    return {
        "type": "channel_module",
        "module_id": cm.module_id,
        "channel_id": cm.channel_id,
        "user_id": cm.user_id,
        "co_host_email": cm.co_host_email,
        "name": cm.name,
        "description": cm.description,
        "cover_image_name": cm.cover_image_name,
        "skills": cm.skills or [],
        "visibility": cm.visibility.value if cm.visibility else None,

        # 🔥 OWNER DETAILS ADDED
        "owner": get_owner_info(db, cm.user_id),
    }


# -----------------------------
# MAIN API
# -----------------------------
@router.get("/")
def get_all_modules(
    search: str = Query(None),
    tag: str = Query(None),
    db: Session = Depends(get_db)
):
    modules = db.query(Module).all()
    channel_modules = db.query(ChannelModule).all()

    data = []

    # ---------------- MODULES ----------------
    for m in modules:
        if search and search.lower() not in (m.name or "").lower():
            continue

        if tag and (not m.skills or tag not in m.skills):
            continue

        data.append(format_module(db, m))

    # ---------------- CHANNEL MODULES ----------------
    for cm in channel_modules:
        if search and search.lower() not in (cm.name or "").lower():
            continue

        if tag and (not cm.skills or tag not in cm.skills):
            continue

        data.append(format_channel_module(db, cm))

    return {
        "count": len(data),
        "data": data
    }