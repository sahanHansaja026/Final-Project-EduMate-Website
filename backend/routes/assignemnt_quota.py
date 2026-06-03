from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from models.assignment import Assignment
from models.module import Module
from models.subscription import Subscription

router = APIRouter(prefix="/quota", tags=["Quota"])


@router.get("/assignment/{user_id}")
def check_assignment_quota(user_id: int, db: Session = Depends(get_db)):

    sub = db.query(Subscription).filter(
        Subscription.user_id == user_id
    ).first()

    plan = "free"
    if sub and sub.plan_name:
        plan = sub.plan_name.value

    is_free = plan == "free"

    assignment_count = (
        db.query(Assignment)
        .join(Module, Assignment.module_id == Module.module_id)
        .filter(Module.user_id == user_id)
        .count()
    )

    limit = 5 if is_free else None
    can_create = not is_free or assignment_count < 5

    return {
        "user_id": user_id,
        "subscription_type": plan,
        "used_assignments": assignment_count,
        "limit": limit,
        "can_create": can_create,
        "remaining": "unlimited" if not is_free else max(0, 5 - assignment_count)
    }