from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.assignment_grade_access import AssignmentGradeAccess

router = APIRouter(prefix="/assignment-grade-access", tags=["AssignmentGradeAccess"])

@router.post("/grant", response_model=dict)
def grant_grade_access(
    assignment_id: int,
    user_id: int,
    db: Session = Depends(get_db),
):
    from app.models.assignment_grade_access import AssignmentGradeAccess
    new_access = AssignmentGradeAccess(
        assignment_id=assignment_id,
        user_id=user_id,
    )
    db.add(new_access)
    db.commit()
    return {"message": "Grade access granted"}

@router.post("/revoke", response_model=dict)
def revoke_grade_access(
    assignment_id: int,
    user_id: int,
    db: Session = Depends(get_db),
):
    from app.models.assignment_grade_access import AssignmentGradeAccess
    access = db.query(AssignmentGradeAccess).filter(
        AssignmentGradeAccess.assignment_id == assignment_id,
        AssignmentGradeAccess.user_id == user_id
    ).first()
    if not access:
        raise HTTPException(status_code=404, detail="Access not found")
    db.delete(access)
    db.commit()
    return {"message": "Grade access revoked"}

@router.get("/assignment/{assignment_id}/user/{user_id}", response_model=bool)
def check_grade_access(
    assignment_id: int,
    user_id: int,
    db: Session = Depends(get_db),
):
    from app.models.assignment_grade_access import AssignmentGradeAccess
    access = db.query(AssignmentGradeAccess).filter(
        AssignmentGradeAccess.assignment_id == assignment_id,
        AssignmentGradeAccess.user_id == user_id
    ).first()
    return {"has_access": access is not None}