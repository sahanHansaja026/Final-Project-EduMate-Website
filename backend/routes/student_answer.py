from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from database import get_db

from models.student_answer import StudentAnswer

from schemas.student_answer import (
    StudentAnswerCreate,
    StudentAnswerResponse
)

router = APIRouter(
    prefix="/student-answers",
    tags=["Student Answers"]
)


# CREATE ANSWER
@router.post("/", response_model=StudentAnswerResponse)
def create_answer(
    answer_data: StudentAnswerCreate,
    db: Session = Depends(get_db)
):

    new_answer = StudentAnswer(
        **answer_data.model_dump()
    )

    db.add(new_answer)
    db.commit()
    db.refresh(new_answer)

    return new_answer


# GET ALL ANSWERS
@router.get("/", response_model=List[StudentAnswerResponse])
def get_answers(db: Session = Depends(get_db)):

    return db.query(StudentAnswer).all()


# GET ANSWERS BY QUIZ
@router.get("/quiz/{quiz_id}",
            response_model=List[StudentAnswerResponse])
def get_answers_by_quiz(
    quiz_id: int,
    db: Session = Depends(get_db)
):

    return db.query(StudentAnswer).filter(
        StudentAnswer.quiz_id == quiz_id
    ).all()


# DELETE ANSWER
@router.delete("/{answer_id}")
def delete_answer(
    answer_id: int,
    db: Session = Depends(get_db)
):

    answer = db.query(StudentAnswer).filter(
        StudentAnswer.id == answer_id
    ).first()

    if not answer:
        raise HTTPException(
            status_code=404,
            detail="Answer not found"
        )

    db.delete(answer)
    db.commit()

    return {
        "message": "Answer deleted successfully"
    }