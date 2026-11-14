from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.subscription_payment import SubscriptionPayment

router = APIRouter(prefix="/subscription-payments", tags=["SubscriptionPayments"])

@router.post("/", response_model=dict, status_code=201)
def create_subscription_payment(
    subscription_id: int,
    amount: float,
    payment_method: str,
    db: Session = Depends(get_db),
):
    from app.models.subscription_payment import SubscriptionPayment
    new_payment = SubscriptionPayment(
        subscription_id=subscription_id,
        amount=amount,
        payment_method=payment_method,
        status="pending",
    )
    db.add(new_payment)
    db.commit()
    db.refresh(new_payment)
    return {"message": "Subscription payment recorded", "payment_id": new_payment.payment_id}

@router.get("/subscription/{subscription_id}", response_model=list)
def get_payments_by_subscription(
    subscription_id: int,
    db: Session = Depends(get_db),
):
    from app.models.subscription_payment import SubscriptionPayment
    payments = db.query(SubscriptionPayment).filter(SubscriptionPayment.subscription_id == subscription_id).all()
    return [{"payment_id": p.payment_id, "amount": p.amount, "status": p.status} for p in payments]