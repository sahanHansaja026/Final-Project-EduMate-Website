from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.chatbot_service import ask_ai

router = APIRouter(
    prefix="/chatbot",
    tags=["AI Chatbot"]
)


# =========================
# Request Schema
# =========================
class ChatRequest(BaseModel):
    message: str


# =========================
# Response Schema
# =========================
class ChatResponse(BaseModel):
    question: str
    answer: str


# =========================
# Chat Endpoint
# =========================
@router.post("/", response_model=ChatResponse)
async def chat_with_ai(payload: ChatRequest):

    if not payload.message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty")

    ai_response = ask_ai(payload.message)

    # optional: fail properly if AI error
    if ai_response.startswith("API Error") or ai_response.startswith("Request Error"):
        raise HTTPException(status_code=500, detail=ai_response)

    return ChatResponse(
        question=payload.message,
        answer=ai_response
    )