from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from models.chaneel_modules import ChannelModule
from database import get_db
from models.quiz import Quiz
from models.module import Module

router = APIRouter(
    prefix="/access-control",
    tags=["Access Control"]
)


@router.get("/quiz/{quiz_id}/user/{user_id}")
def check_quiz_access(
    quiz_id: int,
    user_id: int,
    db: Session = Depends(get_db),
):
    # 1. Get quiz
    quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()

    if not quiz:
        raise HTTPException(
            status_code=404,
            detail=f"Quiz not found (id={quiz_id})"
        )

    # 2. Get module
    module = db.query(Module).filter(
        Module.module_id == quiz.module_id
    ).first()

    if not module:
        raise HTTPException(
            status_code=404,
            detail=f"Module not found (module_id={quiz.module_id})"
        )

    # 3. Access check
    if module.user_id != user_id:
        raise HTTPException(
            status_code=403,
            detail="Access denied: You are not allowed to edit this quiz"
        )

    return {
        "access": True,
        "quiz_id": quiz.id,
        "module_id": module.module_id,
        "owner_id": module.user_id
    }
    
@router.get("/channel-module/quiz/{quiz_id}/user/{user_id}")
def check_channel_module_quiz_access(
    quiz_id: int,
    user_id: int,
    db: Session = Depends(get_db),
):
    # 1. Get quiz
    quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()

    if not quiz:
        raise HTTPException(status_code=404, detail=f"Quiz not found ({quiz_id})")

    # 2. Get channel module from quiz.module_id
    module = db.query(ChannelModule).filter(
        ChannelModule.module_id == quiz.module_id
    ).first()

    if not module:
        raise HTTPException(
            status_code=404,
            detail=f"Channel module not found (module_id={quiz.module_id})"
        )

    # 3. ownership check
    if module.user_id != user_id:
        raise HTTPException(
            status_code=403,
            detail="Access denied: not owner of this channel module quiz"
        )

    return {
        "access": True,
        "quiz_id": quiz.id,
        "module_id": module.module_id,
        "owner_id": module.user_id
    }