from fastapi import APIRouter, Depends, HTTPException, Form
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from database import get_db
from models.quiz import Quiz
from schemas.quiz import QuizResponse

router = APIRouter(prefix="/quizzes", tags=["Quizzes"])


# ✅ CREATE QUIZ
@router.post("/", response_model=QuizResponse)
def create_quiz(
    module_id: int = Form(...),
    title: str = Form(...),
    description: Optional[str] = Form(None),

    attempts: Optional[str] = Form("unlimited"),

    open_date: Optional[datetime] = Form(None),
    close_date: Optional[datetime] = Form(None),

    is_graded: Optional[bool] = Form(True),
    shuffle_questions: Optional[bool] = Form(False),

    db: Session = Depends(get_db),
):
    new_quiz = Quiz(
        module_id=module_id,
        title=title,
        description=description,
        attempts=attempts,
        open_date=open_date,
        close_date=close_date,
        is_graded=is_graded,
        shuffle_questions=shuffle_questions,
    )

    db.add(new_quiz)
    db.commit()
    db.refresh(new_quiz)

    return QuizResponse.from_orm(new_quiz)


# ✅ GET QUIZ BY MODULE
@router.get("/module/{module_id}", response_model=List[QuizResponse])
def get_quizzes_by_module(module_id: int, db: Session = Depends(get_db)):
    quizzes = db.query(Quiz).filter(Quiz.module_id == module_id).all()

    if not quizzes:
        raise HTTPException(status_code=404, detail="No quizzes found")

    return quizzes


# ✅ GET SINGLE QUIZ
@router.get("/{quiz_id}", response_model=QuizResponse)
def get_quiz(quiz_id: int, db: Session = Depends(get_db)):
    quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()

    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")

    return quiz


# ✅ DELETE QUIZ
@router.delete("/{quiz_id}")
def delete_quiz(quiz_id: int, db: Session = Depends(get_db)):
    quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()

    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")

    db.delete(quiz)
    db.commit()

    return {"message": "Quiz deleted successfully"}