"""Authorized-student endpoints for channel modules."""

from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.controllers import authorized_student_controller
from app.core.database import get_db
from app.core.dependencies import get_current_user_optional
from app.models.user import User
from app.schemas.authorized_student import (
    AuthorizedStudentCreate,
    AuthorizedStudentResponse,
    AuthorizedStudentUpdate,
)

router = APIRouter(
    prefix="/authorized-students",
    tags=["Authorized Students"],
)


# add students
@router.post("/", response_model=AuthorizedStudentResponse)
def add_student(
    payload: AuthorizedStudentCreate,
    user_id: int = Query(None),
    current_email: str = Query(None),
    current_user: Optional[User] = Depends(get_current_user_optional),
    db: Session = Depends(get_db),
):
    """Authorize a student for a channel module."""
    return authorized_student_controller.add_student(
        db,
        payload=payload,
        user_id=user_id,
        current_email=current_email,
        current_user=current_user,
    )


# get students by module id
@router.get("/module/{module_id}")
def get_students_by_module(
    module_id: int,
    user_id: int = Query(None),
    current_email: str = Query(None),
    current_user: Optional[User] = Depends(get_current_user_optional),
    db: Session = Depends(get_db),
):
    """Return the students authorized for a module."""
    return authorized_student_controller.get_students_by_module(
        db,
        module_id=module_id,
        user_id=user_id,
        current_email=current_email,
        current_user=current_user,
    )


# delete student
@router.delete("/{student_id}")
def delete_student(
    student_id: int,
    user_id: int = Query(None),
    current_email: str = Query(None),
    current_user: Optional[User] = Depends(get_current_user_optional),
    db: Session = Depends(get_db),
):
    """Remove an authorized student."""
    return authorized_student_controller.delete_student(
        db,
        student_id=student_id,
        user_id=user_id,
        current_email=current_email,
        current_user=current_user,
    )


@router.put("/{student_id}", response_model=AuthorizedStudentResponse)
def update_student(
    student_id: int,
    payload: AuthorizedStudentUpdate,
    user_id: int = Query(None),
    current_email: str = Query(None),
    current_user: Optional[User] = Depends(get_current_user_optional),
    db: Session = Depends(get_db),
):
    """Update an authorized student's status or remark."""
    return authorized_student_controller.update_student(
        db,
        student_id=student_id,
        payload=payload,
        user_id=user_id,
        current_email=current_email,
        current_user=current_user,
    )


@router.get("/{student_id}")
def get_student_by_id(
    student_id: int,
    user_id: int = Query(None),
    current_email: str = Query(None),
    current_user: Optional[User] = Depends(get_current_user_optional),
    db: Session = Depends(get_db),
):
    """Return a single authorized student."""
    student = authorized_student_controller.get_student(
        db,
        student_id=student_id,
        user_id=user_id,
        current_email=current_email,
        current_user=current_user,
    )

    return {
        "id": student.id,
        "channel_module_id": student.channel_module_id,
        "student_name": student.student_name,
        "student_email": student.student_email,
        "admission_date": student.admission_date,
        "status": student.status,
        "remark": student.remark,
    }
