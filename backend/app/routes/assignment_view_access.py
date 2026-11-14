from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.assignment_view_access import AssignmentViewAccess

router = APIRouter(prefix="/assignment-view-access", tags=["AssignmentViewAccess"])

@router.post("/grant", response_model=dict)
def grant_view_access(
    assignment_id: int,
    user_id: int,
    db: Session = Depends(get_db),
):
    from app.models.assignment_view_access import AssignmentViewAccess
    new_access = AssignmentViewAccess(
        assignment_id=assignment_id,
        user_id=user_id,
    )
    db.add(new_access)
    db.commit()
    return {"message": "View access granted"}

@router.post("/revoke", response_model=dict)
def revoke_view_access(
    assignment_id: int,
    user_id: int,
    db: Session = Depends(get_db),
):
    from app.models.assignment_view_access import AssignmentViewAccess
    access = db.query(AssignmentViewAccess).filter(
        AssignmentViewAccess.assignment_id == assignment_id,
        AssignmentViewAccess.user_id == user_id
    ).first()
    if not access:
        raise HTTPException(status_code=404, detail="Access not found")
    db.delete(access)
    db.commit()
    return {"message": "View access revoked"}

@router.get("/assignment/{assignment_id}/user/{user_id}", response_model=bool)
def check_view_access(
    assignment_id: int,
    user_id: int,
    db: Session = Depends(get_db),
):
    from app.models.assignment_view_access import AssignmentViewAccess
    access = db.query(AssignmentViewAccess).filter(
        AssignmentViewAccess.assignment_id == assignment_id,
        AssignmentViewAccess.user_id == user_id
    ).first()
    return {"has_access": access is not None}