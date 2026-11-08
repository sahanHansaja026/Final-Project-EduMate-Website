from fastapi import APIRouter, Depends, HTTPException, status, Form
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.quiz import Quiz
from app.schemas.quiz import QuizResponse
import json

router = APIRouter(prefix="/quizzes", tags=["Quizzes"])

@router.post("/", response_model=QuizResponse, status_code=201)
def create_quiz_endpoint(
    module_id: int = Form(...),
    title: str = Form(...),
    questions: str = Form(...),
    options: str = Form(...),
    correct_answers: str = Form(...),
    db: Session = Depends(get_db),
):
    from app.schemas.quiz import QuizCreateSchema
    
    questions_data = json.loads(questions)
    options_data = json.loads(options)
    correct_answers_data = json.loads(correct_answers)
    
    # Validate module exists
    from app.models.module import Module
    module = db.query(Module).filter(Module.module_id == module_id).first()
    if not module:
        raise HTTPException(status_code=404, detail="Module not found")
    
    new_quiz = Quiz(
        title=title,
        module_id=module_id,
        questions=questions_data,
        options=options_data,
        correct_answers=correct_answers_data,
    )
    db.add(new_quiz)
    db.commit()
    db.refresh(new_quiz)
    return new_quiz

@router.get("/module/{module_id}", response_model=list[QuizResponse])
def get_quizzes_by_module_endpoint(
    module_id: int,
    db: Session = Depends(get_db),
):
    quizzes = db.query(Quiz).filter(Quiz.module_id == module_id).all()
    return quizzes

@router.post("/{quiz_id}/attempt", response_model=dict)
def submit_quiz_attempt_endpoint(
    quiz_id: int,
    answers: str = Form(...),
    db: Session = Depends(get_db),
):
    import json
    answers_data = json.loads(answers)
    
    # Get quiz to check attempt limits
    quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")
    
    # Count existing attempts
    attempt_count = db.query(Quiz).filter(Quiz.id == quiz_id).count()
    
    return {
        "message": "Attempt recorded",
        "quiz_id": quiz_id,
        "attempts_used": attempt_count,
    }

@router.get("/{quiz_id}/attempt/{attempt_id}", response_model=dict)
def get_quiz_attempt_endpoint(
    quiz_id: int,
    attempt_id: int,
    db: Session = Depends(get_db),
):
    attempt = db.query(Quiz).filter(Quiz.id == attempt_id).first()
    if not attempt:
        raise HTTPException(status_code=404, detail="Attempt not found")
    return {"attempt_id": attempt_id, "quiz_id": quiz_id, "title": quiz.title}