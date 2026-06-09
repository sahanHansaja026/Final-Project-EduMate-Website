from fastapi import APIRouter, Depends, HTTPException, Form
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from models.quiz_score import QuizScore
from models.question import Question
from models.question_option import QuestionOption
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

    # 1. delete quiz scores
    db.query(QuizScore).filter(
        QuizScore.quiz_id == quiz_id
    ).delete(synchronize_session=False)

    # 2. find question IDs
    questions = db.query(Question).filter(
        Question.quiz_id == quiz_id
    ).all()

    question_ids = [q.id for q in questions]

    # 3. delete options
    if question_ids:
        db.query(QuestionOption).filter(
            QuestionOption.question_id.in_(question_ids)
        ).delete(synchronize_session=False)

    # 4. delete questions
    db.query(Question).filter(
        Question.quiz_id == quiz_id
    ).delete(synchronize_session=False)

    # 5. delete quiz
    db.delete(quiz)

    db.commit()

    return {"message": "Quiz and all related data deleted successfully"}

@router.put("/{quiz_id}", response_model=QuizResponse)
def update_quiz(
    quiz_id: int,

    title: Optional[str] = Form(None),
    description: Optional[str] = Form(None),

    attempts: Optional[str] = Form(None),

    open_date: Optional[datetime] = Form(None),
    close_date: Optional[datetime] = Form(None),

    is_graded: Optional[bool] = Form(None),
    shuffle_questions: Optional[bool] = Form(None),

    db: Session = Depends(get_db),
):
    quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()

    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")

    # ✅ update only provided fields
    if title is not None:
        quiz.title = title

    if description is not None:
        quiz.description = description

    if attempts is not None:
        quiz.attempts = attempts

    if open_date is not None:
        quiz.open_date = open_date

    if close_date is not None:
        quiz.close_date = close_date

    if is_graded is not None:
        quiz.is_graded = is_graded

    if shuffle_questions is not None:
        quiz.shuffle_questions = shuffle_questions

    db.commit()
    db.refresh(quiz)

    return QuizResponse.from_orm(quiz)