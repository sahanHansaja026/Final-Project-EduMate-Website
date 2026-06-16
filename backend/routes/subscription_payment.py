from fastapi import (
    APIRouter,
    UploadFile,
    File,
    Form,
    Depends,
    HTTPException,
)
from sqlalchemy.orm import Session
from datetime import datetime

from database import get_db
from services.s3_service import upload_file

from models.subscription_payment import (
    SubscriptionPayment,
    PlanEnum,
)

from schemas.subscription_payment import (
    SubscriptionPaymentResponse,
)


router = APIRouter(
    prefix="/subscription",
    tags=["Subscription"]
)


@router.post(
    "/submit-slip",
    response_model=SubscriptionPaymentResponse
)
async def submit_subscription_slip(
    user_id: int = Form(...),
    user_email: str = Form(...),

    plan_type: PlanEnum = Form(...),

    start_date: str = Form(...),
    valid_period: str = Form(...),

    expire_date: str = Form(...),

    transaction_reference: str = Form(...),

    receipt_file: UploadFile = File(...),

    db: Session = Depends(get_db),
):
    
    if not user_email.strip():
        raise HTTPException(
            status_code=400,
            detail="User email is required."
        )

    if not transaction_reference.strip():
        raise HTTPException(
            status_code=400,
            detail="Transaction reference is required."
        )

    if not receipt_file:
        raise HTTPException(
            status_code=400,
            detail="Receipt file is required."
        )

    allowed_types = [
        "image/jpeg",
        "image/jpg",
        "image/png",
        "application/pdf",
    ]

    if receipt_file.content_type not in allowed_types:
        raise HTTPException(
            status_code=400,
            detail="Only JPG, JPEG, PNG and PDF files are allowed."
        )

    try:
        receipt_url = upload_file(
            receipt_file,
            folder="subscription-receipts"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to upload receipt: {str(e)}"
        )

    try:
        payment = SubscriptionPayment(
            user_id=user_id,
            user_email=user_email,

            plan_name=plan_type,

            start_date=datetime.fromisoformat(start_date),
            end_date=datetime.fromisoformat(expire_date),

            transaction_reference=transaction_reference,

            receipt_file=receipt_url,

            status="pending",
        )

        db.add(payment)
        db.commit()
        db.refresh(payment)

        return payment

    except Exception as e:
        db.rollback()

        raise HTTPException(
            status_code=500,
            detail=f"Failed to save subscription payment: {str(e)}"
        )