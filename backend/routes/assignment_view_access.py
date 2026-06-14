from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models.assignment import Assignment
from models.chaneel_modules import ChannelModule
from models.authorized_student import AuthorizedStudent

router = APIRouter(prefix="/assignment-access", tags=["Assignment Access"])


@router.get("/check")
def check_assignment_access(
    assignment_id: int,
    user_id: int,
    user_email: str,
    db: Session = Depends(get_db),
):
    # 1. Get assignment
    assignment = db.query(Assignment).filter(
        Assignment.id == assignment_id
    ).first()

    if not assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")

    # 2. Get module
    module = db.query(ChannelModule).filter(
        ChannelModule.module_id == assignment.module_id
    ).first()

    if not module:
        raise HTTPException(status_code=404, detail="Module not found")

    # ---------------------------------------
    # 3. OWNER CHECK
    # ---------------------------------------
    if module.user_id == user_id:
        return {
            "access": True,
            "reason": "module_owner"
        }

    # ---------------------------------------
    # 4. AUTHORIZED STUDENT CHECK
    # ---------------------------------------
    student = db.query(AuthorizedStudent).filter(
        AuthorizedStudent.channel_module_id == module.module_id,
        AuthorizedStudent.student_email == user_email
    ).first()

    if student:
        return {
            "access": True,
            "reason": "authorized_student"
        }

    # ---------------------------------------
    # 5. DENY ACCESS
    # ---------------------------------------
    return {
        "access": False,
        "reason": "not_authorized"
    }