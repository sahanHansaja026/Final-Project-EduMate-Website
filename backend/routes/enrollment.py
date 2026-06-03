from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from database import get_db

from models.enrollment import Enrollment
from schemas.enrollment import (
    EnrollmentCreate,
    EnrollmentUpdate,
    EnrollmentResponse
)

router = APIRouter(
    prefix="/enrollments",
    tags=["Enrollments"]
)

# create 
@router.post("/", response_model=EnrollmentResponse)
def create_enrollment(
    data: EnrollmentCreate,
    db: Session = Depends(get_db)
):

    # prevent duplicate enrollment
    existing = db.query(Enrollment).filter(
        Enrollment.user_id == data.user_id,
        Enrollment.module_id == data.module_id
    ).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail="User already enrolled in this module"
        )

    enrollment = Enrollment(
        user_id=data.user_id,
        module_id=data.module_id
    )

    db.add(enrollment)
    db.commit()
    db.refresh(enrollment)

    return enrollment

# get all
@router.get("/", response_model=List[EnrollmentResponse])
def get_all_enrollments(db: Session = Depends(get_db)):
    return db.query(Enrollment).all()

# get by user
@router.get("/user/{user_id}", response_model=List[EnrollmentResponse])
def get_user_enrollments(user_id: int, db: Session = Depends(get_db)):

    return db.query(Enrollment).filter(
        Enrollment.user_id == user_id
    ).all()
    
# get by model
@router.get("/module/{module_id}", response_model=List[EnrollmentResponse])
def get_module_enrollments(module_id: int, db: Session = Depends(get_db)):

    return db.query(Enrollment).filter(
        Enrollment.module_id == module_id
    ).all()
    
# update status
@router.put("/{enrollment_id}", response_model=EnrollmentResponse)
def update_enrollment(
    enrollment_id: int,
    data: EnrollmentUpdate,
    db: Session = Depends(get_db)
):

    enrollment = db.query(Enrollment).filter(
        Enrollment.enrollment_id == enrollment_id
    ).first()

    if not enrollment:
        raise HTTPException(status_code=404, detail="Enrollment not found")

    enrollment.completed = data.completed

    db.commit()
    db.refresh(enrollment)

    return enrollment