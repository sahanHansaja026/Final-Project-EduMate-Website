from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from models.subscription import Subscription
from models.module import Module
from models.video import Video

router = APIRouter(prefix="/quota", tags=["Video Quota"])


# =========================
# VIDEO QUOTA CHECK (FREE = 1 VIDEO)
# =========================

@router.get("/video/{user_id}")
def check_video_quota(user_id: int, db: Session = Depends(get_db)):

    # 1. Get subscription
    sub = db.query(Subscription).filter(
        Subscription.user_id == user_id
    ).first()

    plan = "free"
    if sub:
        plan = getattr(sub, "plan", None) or getattr(sub, "plan_type", None) or "free"

    is_free = plan.lower() == "free"

    # 2. Count videos via MODULE -> USER relationship
    video_count = (
        db.query(Video)
        .join(Module, Video.module_id == Module.module_id)
        .filter(Module.user_id == user_id)
        .count()
    )

    # 3. Rule
    limit = 1 if is_free else None
    can_create = True

    if is_free:
        can_create = video_count < 1

    return {
        "user_id": user_id,
        "subscription_type": plan,
        "used_videos": video_count,
        "limit": limit,
        "can_create": can_create,
        "remaining": 0 if is_free and video_count >= 1 else "unlimited"
    }