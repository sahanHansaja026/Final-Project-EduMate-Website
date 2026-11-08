from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db

router = APIRouter(prefix="/chatbot", tags=["Chatbot"])

@router.post("/ask", response_model=dict)
def ask_question(
    question: str,
    db: Session = Depends(get_db),
):
    from app.services.chatbot_service import process_chatbot_question
    result = process_chatbot_question(question, db)
    return result

@router.get("/history", response_model=list)
def get_chat_history(
    db: Session = Depends(get_db),
):
    from app.services.chatbot_service import get_chat_history as gh
    return gh(db)