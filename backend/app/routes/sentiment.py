from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.sentiment import SentimentAnalysis

router = APIRouter(prefix="/sentiment", tags=["Sentiment"])

@router.post("/analyze", response_model=dict)
def analyze_sentiment(
    text: str,
    db: Session = Depends(get_db),
):
    from app.models.sentiment import SentimentAnalysis
    new_analysis = SentimentAnalysis(
        text=text,
    )
    db.add(new_analysis)
    db.commit()
    db.refresh(new_analysis)
    return {
        "sentiment": new_analysis.sentiment,
        "confidence": new_analysis.confidence,
    }

@router.get("/history/{user_id}", response_model=list)
def get_sentiment_history(
    user_id: int,
    db: Session = Depends(get_db),
):
    from app.models.sentiment import SentimentAnalysis
    analyses = db.query(SentimentAnalysis).all()
    return [{"text": a.text, "sentiment": a.sentiment, "created_at": str(a.created_at)} for a in analyses]