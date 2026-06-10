from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from database import get_db
from models.module import Module
from models.enrollment import Enrollment

router = APIRouter(
    prefix="/enrollment-analytics",
    tags=["Enrollment Analytics"]
)


# ==========================
# MODULES + ENROLLMENT COUNT
# ==========================
@router.get("/teacher/{user_id}")
def get_teacher_module_enrollments(
    user_id: int,
    db: Session = Depends(get_db)
):
    modules = (
        db.query(
            Module.module_id,
            Module.name,
            func.count(Enrollment.enrollment_id).label("student_count")
        )
        .outerjoin(
            Enrollment,
            Module.module_id == Enrollment.module_id
        )
        .filter(
            Module.user_id == user_id
        )
        .group_by(
            Module.module_id,
            Module.name
        )
        .all()
    )

    return [
        {
            "module_id": module.module_id,
            "module_name": module.name,
            "student_count": module.student_count
        }
        for module in modules
    ]


# ==========================
# TOTAL ENROLLMENTS
# ==========================
@router.get("/teacher/{user_id}/total")
def get_total_enrollments(
    user_id: int,
    db: Session = Depends(get_db)
):
    total = (
        db.query(func.count(Enrollment.enrollment_id))
        .join(
            Module,
            Module.module_id == Enrollment.module_id
        )
        .filter(
            Module.user_id == user_id
        )
        .scalar()
    )

    return {
        "teacher_id": user_id,
        "total_enrollments": total
    }


# ==========================
# TOP ENROLLED MODULE
# ==========================
@router.get("/teacher/{user_id}/top-module")
def get_top_module(
    user_id: int,
    db: Session = Depends(get_db)
):
    result = (
        db.query(
            Module.module_id,
            Module.name,
            func.count(Enrollment.enrollment_id).label("student_count")
        )
        .outerjoin(
            Enrollment,
            Module.module_id == Enrollment.module_id
        )
        .filter(
            Module.user_id == user_id
        )
        .group_by(
            Module.module_id,
            Module.name
        )
        .order_by(
            func.count(Enrollment.enrollment_id).desc()
        )
        .first()
    )

    if not result:
        return {
            "module_id": None,
            "module_name": None,
            "student_count": 0
        }

    return {
        "module_id": result.module_id,
        "module_name": result.name,
        "student_count": result.student_count
    }