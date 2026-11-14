from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.module_quiz_access_controller import ModuleQuizAccessController

router = APIRouter(prefix="/module-quiz-access", tags=["ModuleQuizAccess"])

@router.post("/grant", response_model=dict)
def grant_quiz_access(
    module_id: int,
    quiz_id: int,
    user_id: int,
    db: Session = Depends(get_db),
):
    from app.models.module_quiz_access_controller import ModuleQuizAccessController
    # Check if already granted
    existing = db.query(ModuleQuizAccessController).filter(
        ModuleQuizAccessController.module_id == module_id,
        ModuleQuizAccessController.quiz_id == quiz_id,
        ModuleQuizAccessController.user_id == user_id
    ).first()
    if existing:
        return {"message": "Quiz access already granted"}
    
    new_access = ModuleQuizAccessController(
        module_id=module_id,
        quiz_id=quiz_id,
        user_id=user_id,
    )
    db.add(new_access)
    db.commit()
    return {"message": "Quiz access granted"}

@router.post("/revoke", response_model=dict)
def revoke_quiz_access(
    module_id: int,
    quiz_id: int,
    user_id: int,
    db: Session = Depends(get_db),
):
    from app.models.module_quiz_access_controller import ModuleQuizAccessController
    access = db.query(ModuleQuizAccessController).filter(
        ModuleQuizAccessController.module_id == module_id,
        ModuleQuizAccessController.quiz_id == quiz_id,
        ModuleQuizAccessController.user_id == user_id
    ).first()
    if not access:
        raise HTTPException(status_code=404, detail="Access not found")
    
    db.delete(access)
    db.commit()
    return {"message": "Quiz access revoked"}

@router.get("/module/{module_id}/quiz/{quiz_id}", response_model=bool)
def check_quiz_access(
    module_id: int,
    quiz_id: int,
    user_id: int,
    db: Session = Depends(get_db),
):
    from app.models.module_quiz_access_controller import ModuleQuizAccessController
    access = db.query(ModuleQuizAccessController).filter(
        ModuleQuizAccessController.module_id == module_id,
        ModuleQuizAccessController.quiz_id == quiz_id,
        ModuleQuizAccessController.user_id == user_id
    ).first()
    return {"has_access": access is not None}