from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.enrollment import Enrollment

router = APIRouter(prefix="/enrollments", tags=["Enrollments"])

@router.post("/", response_model=dict, status_code=201)
def enroll_user_in_module(
    user_id: int,
    module_id: int,
    db: Session = Depends(get_db),
):
    from app.models.enrollment import Enrollment
    # Check if already enrolled
    existing = db.query(Enrollment).filter(
        Enrollment.user_id == user_id,
        Enrollment.module_id == module_id
    ).first()
    if existing:
        return {"message": "User already enrolled in this module"}
    
    new_enrollment = Enrollment(
        user_id=user_id,
        module_id=module_id,
    )
    db.add(new_enrollment)
    db.commit()
    db.refresh(new_enrollment)
    return {"message": "User enrolled successfully", "enrollment_id": new_enrollment.enrollment_id}

@router.get("/user/{user_id}", response_model=list)
def get_user_enrollments(
    user_id: int,
    db: Session = Depends(get_db),
):
    from app.models.enrollment import Enrollment
    enrollments = db.query(Enrollment).filter(Enrollment.user_id == user_id).all()
    return [{"enrollment_id": e.enrollment_id, "module_id": e.module_id} for e in enrollments]

@router.get("/module/{module_id}", response_model=list)
def get_module_enrollments(
    module_id: int,
    db: Session = Depends(get_db),
):
    from app.models.enrollment import Enrollment
    enrollments = db.query(Enrollment).filter(Enrollment.module_id == module_id).all()
    return [{"enrollment_id": e.enrollment_id, "user_id": e.user_id} for e in enrollments]