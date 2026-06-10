from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models.authorized_student import AuthorizedStudent

router = APIRouter(
    prefix="/channel-module-access",
    tags=["Channel Module Access"]
)

@router.get("/check/{module_id}/{student_email}")
def check_module_access(
    module_id: int,
    student_email: str,
    db: Session = Depends(get_db)
):
    student = db.query(AuthorizedStudent).filter(
        AuthorizedStudent.channel_module_id == module_id,
        AuthorizedStudent.student_email == student_email
    ).first()

    # CASE 1: student not found
    if not student:
        raise HTTPException(
            status_code=403,
            detail="Access denied: Student not enrolled in this module"
        )

    # CASE 2: suspended student
    if student.status != "active":
        raise HTTPException(
            status_code=403,
            detail="Access denied: Student is suspended"
        )

    return {
        "access": True,
        "student_name": student.student_name,
        "module_id": module_id
    }