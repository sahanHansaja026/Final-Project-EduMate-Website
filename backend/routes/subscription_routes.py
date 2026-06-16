from typing import Optional
from fastapi import APIRouter, Depends, Form, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime, timedelta, timezone

# Platform Database & Schema Dependencies
from database import get_db
from models.subscription import Subscription
from schemas.subscription import SubscriptionResponse
from routes.access_control import can_access

router = APIRouter(prefix="/subscription", tags=["Subscription"])


# ─── GET USER SUBSCRIPTION PROFILE ───────────────────────────────────────────
@router.get("/{user_id}", response_model=SubscriptionResponse)
def get_subscription(user_id: int, db: Session = Depends(get_db)):
    """
    Fetches the active or basic subscription record profile for a specific user.
    """
    sub = db.query(Subscription).filter(Subscription.user_id == user_id).first()
    
    if not sub:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Subscription record profile not found for this user."
        )
        
    return sub


# ─── CHECK MODULE / RESOURCE ACCESS ──────────────────────────────────────────
@router.get("/check/{user_id}")
def check_access(
    user_id: int,
    resource_type: str,
    resource_name: str,
    db: Session = Depends(get_db)
):
    """
    Validates limits dynamically for features (videos, modules, quizzes, channels)
    before permitting mutation operations on the frontend layout.
    """
    sub = db.query(Subscription).filter(Subscription.user_id == user_id).first()

    if not sub:
        return {"access": False, "detail": "No active membership tracking record found."}

    # Evaluate using localized domain rules in access_control system module
    access = can_access(sub, resource_type, resource_name)

    return {
        "user_id": user_id,
        "access": access
    }


# ─── DYNAMIC SUBSCRIPTION PLAN UPDATE UPGRADES ─────────────────────────────
@router.put("/update/{user_id}")
def update_subscription(
    user_id: int,
    subscription_type: str = Form(...),          # Expects: "free", "premium", or "edu"
    status: str = Form(...),                     # Expects: "active", "suspended", etc.
    billing_cycle: Optional[str] = Form(None),   # Expects: "1m" or "6m" for professional tiers
    db: Session = Depends(get_db)
):
    """
    Updates the target plan structure tier, adjusting expiration metrics 
    dynamically matching duration configuration metrics.
    """
    sub = db.query(Subscription).filter(Subscription.user_id == user_id).first()

    if not sub:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Subscription target reference does not exist for configuration updating."
        )

    # 1. Map Core Entity Plan Assignments
    sub.plan_name = subscription_type.lower().strip()
    sub.status = status.lower().strip()

    # 2. Reset Timeline Framework Calculations (Standard Naive UTC format)
    now = datetime.now(timezone.utc).replace(tzinfo=None) 
    sub.start_date = now

    # 3. Dynamic Duration Assignment 
    if sub.plan_name == "premium":
        if billing_cycle == "6m":
            sub.end_date = now + timedelta(days=180)    # Professional Teacher (6 Months) -> 2,500 LKR
        else:
            sub.end_date = now + timedelta(days=30)     # Professional Teacher (1 Month)  -> 500 LKR
            
    elif sub.plan_name == "edu":
        sub.end_date = now + timedelta(days=365)        # Campus Institutional (1 Year)   -> 25,000 LKR
        
    else:
        # Default fallback standard baseline tier (Unlimited/Lifetime duration reference)
        sub.end_date = now + timedelta(days=36500)      # ~100 Years baseline safety block

    # 4. Save and return changes
    db.commit()
    db.refresh(sub)

    return {
        "status": "success",
        "message": f"Subscription successfully mapped to {sub.plan_name.upper()}",
        "data": {
            "user_id": sub.user_id,
            "plan_name": sub.plan_name,
            "status": sub.status,
            "start_date": sub.start_date.isoformat() if sub.start_date else None,
            "end_date": sub.end_date.isoformat() if sub.end_date else None
        }
    }