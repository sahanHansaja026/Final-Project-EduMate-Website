from fastapi import APIRouter, Depends, HTTPException, Form
from sqlalchemy.orm import Session

from database import get_db
from models.assignment import Assignment
from models.chaneel_modules import ChannelModule

router = APIRouter(prefix="/assignment-access", tags=["Assignment Access"])


@router.post("/check")
def check_assignment_access(
    assignment_id: int = Form(...),
    current_user_id: int = Form(...),
    db: Session = Depends(get_db),
):
    # 1. Get assignment
    assignment = (
        db.query(Assignment)
        .filter(Assignment.id == assignment_id)
        .first()
    )

    if not assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")

    # 2. Get module
    module = (
        db.query(ChannelModule)
        .filter(ChannelModule.module_id == assignment.module_id)
        .first()
    )

    if not module:
        raise HTTPException(status_code=404, detail="Module not found")

    # 3. Check ownership
    if module.user_id != current_user_id:
        raise HTTPException(
            status_code=403,
            detail="You do not have permission to access this assignment"
        )

    return {
        "access": True,
        "message": "Access granted",
        "assignment_id": assignment_id,
        "module_id": module.module_id
    }

