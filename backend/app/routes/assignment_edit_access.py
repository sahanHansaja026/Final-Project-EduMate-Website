from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.assignment_edit_access import AssignmentEditAccess

router = APIRouter(prefix="/assignment-edit-access", tags=["AssignmentEditAccess"])

@router.post("/grant", response_model=dict)
def grant_edit_access(
    assignment_id: int,
    user_id: int,
    db: Session = Depends(get_db),
):
    from app.models.assignment_edit_access import AssignmentEditAccess
    # Check if already granted
    existing = db.query(AssignmentEditAccess).filter(
        AssignmentEditAccess.assignment_id == assignment_id,
        AssignmentEditAccess.user_id == user_id
    ).first()
    if existing:
        return {"message": "Edit access already granted"}
    
    new_access = AssignmentEditAccess(
        assignment_id=assignment_id,
        user_id=user_id,
    )
    db.add(new_access)
    db.commit()
    return {"message": "Edit access granted"}

@router.post("/revoke", response_model=dict)
def revoke_edit_access(
    assignment_id: int,
    user_id: int,
    db: Session = Depends(get_db),
):
    from app.models.assignment_edit_access import AssignmentEditAccess
    access = db.query(AssignmentEditAccess).filter(
        AssignmentEditAccess.assignment_id == assignment_id,
        AssignmentEditAccess.user_id == user_id
    ).first()
    if not access:
        raise HTTPException(status_code=404, detail="Access not found")
    
    db.delete(access)
    db.commit()
    return {"message": "Edit access revoked"}

@router.get("/assignment/{assignment_id}/user/{user_id}", response_model=bool)
def check_edit_access(
    assignment_id: int,
    user_id: int,
    db: Session = Depends(get_db),
):
    from app.models.assignment_edit_access import AssignmentEditAccess
    access = db.query(AssignmentEditAccess).filter(
        AssignmentEditAccess.assignment_id == assignment_id,
        AssignmentEditAccess.user_id == user_id
    ).first()
    return {"has_access": access is not None}