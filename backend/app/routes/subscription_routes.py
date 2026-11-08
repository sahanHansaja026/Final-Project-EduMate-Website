from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.subscription import Subscription, PlanEnum

router = APIRouter(prefix="/subscriptions", tags=["Subscriptions"])

@router.get("/user/{user_id}", response_model=dict)
def get_user_subscription(
    user_id: int,
    db: Session = Depends(get_db),
):
    from app.models.subscription import Subscription
    subscription = db.query(Subscription).filter(Subscription.user_id == user_id).first()
    if not subscription:
        return {"plan": "free", "status": "active", "message": "No subscription found, user on free plan"}
    
    return {
        "plan": subscription.plan_name,
        "status": subscription.status,
        "start_date": str(subscription.start_date),
        "end_date": str(subscription.end_date),
    }

@router.post("/upgrade", response_model=dict)
def upgrade_subscription(
    user_id: int,
    new_plan: PlanEnum,
    db: Session = Depends(get_db),
):
    from app.models.subscription import Subscription
    from datetime import datetime, timedelta
    
    subscription = db.query(Subscription).filter(Subscription.user_id == user_id).first()
    if not subscription:
        subscription = Subscription(
            user_id=user_id,
            plan_name=new_plan,
            start_date=datetime.utcnow(),
            end_date=datetime.utcnow() + timedelta(days=30),
            status="active"
        )
        db.add(subscription)
    else:
        subscription.plan_name = new_plan
        subscription.status = "active"
        subscription.start_date = datetime.utcnow()
        subscription.end_date = datetime.utcnow() + timedelta(days=30)
    
    db.commit()
    return {"message": f"Subscription upgraded to {new_plan}"}

@router.post("/cancel", response_model=dict)
def cancel_subscription(
    user_id: int,
    db: Session = Depends(get_db),
):
    from app.models.subscription import Subscription
    subscription = db.query(Subscription).filter(Subscription.user_id == user_id).first()
    if not subscription:
        raise HTTPException(status_code=404, detail="Subscription not found")
    
    subscription.status = "cancelled"
    db.commit()
    return {"message": "Subscription cancelled"}