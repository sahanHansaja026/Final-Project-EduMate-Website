from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from models.subscription import Subscription
from models.module import Module

router = APIRouter(prefix="/quota", tags=["Module Quota"])


# =========================
# MODULE CREATION LIMIT CHECK
# =========================

@router.get("/module/{user_id}")
def check_module_quota(user_id: int, db: Session = Depends(get_db)):

    # 1. Get subscription
    sub = db.query(Subscription).filter(
        Subscription.user_id == user_id
    ).first()

    # If no subscription → treat as free
    if not sub:
        plan = "free"
    else:
        # 🔥 adjust this based on your DB field
        plan = getattr(sub, "plan", None) or getattr(sub, "plan_type", None) or "free"

    # 2. Get module count
    module_count = db.query(Module).filter(
        Module.user_id == user_id
    ).count()

    # 3. Define limits
    is_free = plan.lower() == "free"

    if is_free:
        limit = 1
    else:
        limit = None  # unlimited

    # 4. Access logic
    if is_free:
        can_create = module_count < 1
    else:
        can_create = True

    return {
        "user_id": user_id,
        "subscription_type": plan,
        "used_modules": module_count,
        "limit": limit,
        "can_create": can_create,
        "remaining": 0 if is_free and module_count >= 1 else "unlimited"
    }