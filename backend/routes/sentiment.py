from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import joblib
import os

from database import get_db
from models.module import Module
from models.comment import Comment

router = APIRouter(
    prefix="/sentiment",
    tags=["Sentiment Analysis"]
)

# =========================
# LOAD MODEL + VECTORIZER
# =========================
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

MODEL_PATH = os.path.join(BASE_DIR, "trainmodels", "model.pkl")
VECTORIZER_PATH = os.path.join(BASE_DIR, "trainmodels", "vectorizer.pkl")

model = joblib.load(MODEL_PATH)
vectorizer = joblib.load(VECTORIZER_PATH)


# =========================
# SENTIMENT ENDPOINT
# =========================
@router.get("/module-owner/{user_id}")
def get_comments_with_sentiment(
    user_id: int,
    db: Session = Depends(get_db)
):
    # 1. Get modules owned by user
    modules = db.query(Module.module_id).filter(Module.user_id == user_id).all()
    module_ids = [m[0] for m in modules]

    if not module_ids:
        return {
            "owner_user_id": user_id,
            "total_comments": 0,
            "positive": 0,
            "negative": 0,
            "comments": []
        }

    # 2. Get comments + module name
    comments = db.query(Comment, Module.name).join(
        Module, Comment.module_id == Module.module_id
    ).filter(
        Comment.module_id.in_(module_ids)
    ).all()

    if not comments:
        return {
            "owner_user_id": user_id,
            "total_comments": 0,
            "positive": 0,
            "negative": 0,
            "comments": []
        }

    # ==========================================
    # 3. BATCH PREDICTION (Much faster!)
    # ==========================================
    texts = [comment.text or "" for comment, _ in comments]
    
    # Transform and predict all texts in one go
    vec_matrix = vectorizer.transform(texts)
    predictions = model.predict(vec_matrix)

    results = []
    positive_count = 0
    negative_count = 0

    # 4. Build results
    for i, (comment, module_name) in enumerate(comments):
        pred = predictions[i]

        # ADJUST THIS CONDITION BASED ON YOUR DEBUG PRINT
        # Change to `pred == "positive"` or `pred == "1"` if needed
        is_positive = (pred == 1 or str(pred).lower() in ["1", "positive", "pos"])

        if is_positive:
            sentiment = "Positive"
            positive_count += 1
        else:
            sentiment = "Negative"
            negative_count += 1

        results.append({
            "comment_id": comment.id,
            "module_id": comment.module_id,
            "module_name": module_name,
            "user_id": comment.user_id,
            "text": texts[i],
            "sentiment": sentiment
        })

    return {
        "owner_user_id": user_id,
        "total_comments": len(results),
        "positive": positive_count,
        "negative": negative_count,
        "comments": results
    }