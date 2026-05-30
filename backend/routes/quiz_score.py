from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from database import get_db

from models.quiz_score import QuizScore

from schemas.quiz_score import (
    QuizScoreCreate,
    QuizScoreResponse
)

router = APIRouter(
    prefix="/quiz-scores",
    tags=["Quiz Scores"]
)


# CREATE SCORE
@router.post("/", response_model=QuizScoreResponse)
def create_score(
    score_data: QuizScoreCreate,
    db: Session = Depends(get_db)
):

    new_score = QuizScore(**score_data.model_dump())

    db.add(new_score)
    db.commit()
    db.refresh(new_score)

    return new_score


# GET ALL SCORES
@router.get("/", response_model=List[QuizScoreResponse])
def get_all_scores(db: Session = Depends(get_db)):

    return db.query(QuizScore).all()


# GET SCORE BY ID
@router.get("/{score_id}", response_model=QuizScoreResponse)
def get_score(score_id: int, db: Session = Depends(get_db)):

    score = db.query(QuizScore).filter(
        QuizScore.id == score_id
    ).first()

    if not score:
        raise HTTPException(
            status_code=404,
            detail="Score not found"
        )

    return score


# DELETE SCORE
@router.delete("/{score_id}")
def delete_score(score_id: int, db: Session = Depends(get_db)):

    score = db.query(QuizScore).filter(
        QuizScore.id == score_id
    ).first()

    if not score:
        raise HTTPException(
            status_code=404,
            detail="Score not found"
        )

    db.delete(score)
    db.commit()

    return {"message": "Score deleted successfully"}

# GET SCORE BY QUIZ ID AND USER ID
@router.get(
    "/quiz/{quiz_id}/user/{student_id}",
    response_model=List[QuizScoreResponse]
)
def get_score_by_quiz_and_user(
    quiz_id: int,
    student_id: int,
    db: Session = Depends(get_db)
):

    scores = db.query(QuizScore).filter(
        QuizScore.quiz_id == quiz_id,
        QuizScore.student_id == student_id
    ).all()

    if not scores:
        raise HTTPException(
            status_code=404,
            detail="No scores found"
        )

    return scores

# GET SCORES BY QUIZ ID
@router.get(
    "/quiz/{quiz_id}",
    response_model=List[QuizScoreResponse]
)
def get_scores_by_quiz(
    quiz_id: int,
    db: Session = Depends(get_db)
):

    scores = db.query(QuizScore).filter(
        QuizScore.quiz_id == quiz_id
    ).all()

    if not scores:
        raise HTTPException(
            status_code=404,
            detail="No scores found"
        )

    return scores