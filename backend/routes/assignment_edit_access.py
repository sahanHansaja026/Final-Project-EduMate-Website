from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from models.chaneel_modules import ChannelModule
from database import get_db
from models.assignment import Assignment
from models.module import Module

router = APIRouter(prefix="/assignment-access", tags=["Assignment Access"])


@router.get("/can-edit")
def can_edit_assignment(
    assignment_id: int,
    current_user_id: int,
    db: Session = Depends(get_db),
):
    # 1. Get assignment
    assignment = db.query(Assignment).filter(
        Assignment.id == assignment_id
    ).first()

    if not assignment:
        raise HTTPException(
            status_code=404,
            detail="Assignment not found"
        )

    # 2. Get module
    module = db.query(Module).filter(
        Module.module_id == assignment.module_id
    ).first()

    if not module:
        raise HTTPException(
            status_code=404,
            detail="Module not found for this assignment"
        )

    # 3. Ownership check
    if module.user_id != current_user_id:
        return {
            "access": False,
            "message": "You are not authorized to edit this assignment"
        }

    return {
        "access": True,
        "message": "Access granted"
    }
    
    # =========================
# CHANNEL MODULE EDIT ACCESS
# =========================
@router.get("/channel-module/edit")
def can_edit_channel_module(
    module_id: int,
    current_user_id: int,
    db: Session = Depends(get_db),
):
    module = db.query(ChannelModule).filter(
        ChannelModule.module_id == module_id
    ).first()

    if not module:
        raise HTTPException(status_code=404, detail="Channel module not found")

    if module.user_id != current_user_id:
        return {
            "access": False,
            "message": "Not authorized to edit this channel module"
        }

    return {
        "access": True,
        "message": "Access granted"
    }