from fastapi import APIRouter, Depends, HTTPException, Form
from sqlalchemy.orm import Session

from database import get_db
from models.assignment import Assignment
from models.module import Module  # <-- your new model

router = APIRouter(prefix="/module-access", tags=["Module Access"])


@router.post("/check")
def check_module_access(
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

    # 2. Get module from assignment
    module = (
        db.query(Module)
        .filter(Module.module_id == assignment.module_id)
        .first()
    )

    if not module:
        raise HTTPException(status_code=404, detail="Module not found")

    # 3. Check ownership (module owner)
    if module.user_id != current_user_id:
        raise HTTPException(
            status_code=403,
            detail="You are not allowed to access this module assignment"
        )

    return {
        "access": True,
        "message": "Module access granted",
        "module_id": module.module_id,
        "assignment_id": assignment_id
    }