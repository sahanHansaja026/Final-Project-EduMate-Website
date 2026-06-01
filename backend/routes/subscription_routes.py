from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models.subscription import Subscription
from schemas.subscription import SubscriptionResponse

from routes.access_control import can_access

router = APIRouter(prefix="/subscription", tags=["Subscription"])


@router.get("/{user_id}", response_model=SubscriptionResponse)
def get_subscription(user_id: int, db: Session = Depends(get_db)):

    sub = db.query(Subscription).filter(
        Subscription.user_id == user_id
    ).first()

    if not sub:
        raise HTTPException(status_code=404, detail="Subscription not found")

    return sub


@router.get("/check/{user_id}")
def check_access(
    user_id: int,
    resource_type: str,
    resource_name: str,
    db: Session = Depends(get_db)
):

    sub = db.query(Subscription).filter(
        Subscription.user_id == user_id
    ).first()

    if not sub:
        return {"access": False}

    access = can_access(sub, resource_type, resource_name)

    return {
        "user_id": user_id,
        "access": access
    }



# 🔥 CHECK ACCESS (IMPORTANT FOR FRONTEND)
@router.get("/check/{user_id}")
def check_access(
    user_id: int,
    resource_type: str,
    resource_name: str,
    db: Session = Depends(get_db)
):

    sub = db.query(Subscription).filter(
        Subscription.user_id == user_id
    ).first()

    if not sub:
        return {"access": False}

    access = can_access(sub, resource_type, resource_name)

    return {
        "user_id": user_id,
        "access": access
    }