from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.question import Question
from app.schemas.question import QuestionCreate
from app.models.quiz import Quiz

router = APIRouter(prefix="/questions", tags=["Questions"])

@router.post("/", response_model=dict, status_code=201)
def create_question(
    text: str,
    question_type: str,
    quiz_id: int,
    db: Session = Depends(get_db),
):
    # Validate quiz exists
    quiz = db.query(Quiz).filter(Quiz.quiz_id == quiz_id).first()
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")
    
    new_question = Question(
        text=text,
        question_type=question_type,
        quiz_id=quiz_id,
    )
    db.add(new_question)
    db.commit()
    db.refresh(new_question)
    
    return {"message": "Question created", "question_id": new_question.question_id}

@router.post("/{question_id}/options", response_model=dict, status_code=201)
def create_question_options(
    question_id: int,
    options: str,
    is_correct: str,
    db: Session = Depends(get_db),
):
    import json
    
    option_data = json.loads(options)
    is_correct_data = json.loads(is_correct)
    
    for i, option in enumerate(option_data):
        # Create option as a simple dict since QuestionOption model doesn't exist
        option_record = {
            "question_id": question_id,
            "text": option,
            "is_correct": is_correct_data[i] if i < len(is_correct_data) else False,
        }
        # Store as JSON or create a simple model
        from json import dumps
        db.execute(
            f"INSERT INTO questions_options (question_id, text, is_correct) VALUES ({question_id}, '{option}', {is_correct_data[i] if i < len(is_correct_data) else False})"
        )
    
    db.commit()
    return {"message": "Options created successfully"}

@router.get("/{question_id}", response_model=dict)
def get_question(
    question_id: int,
    db: Session = Depends(get_db),
):
    question = db.query(Question).filter(Question.id == question_id).first()
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    return {
        "question_id": question.id,
        "text": question.question_text,
        "question_type": question.question_type,
    }