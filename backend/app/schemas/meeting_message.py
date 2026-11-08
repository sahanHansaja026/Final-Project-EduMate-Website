from pydantic import BaseModel

class MessageCreate(BaseModel):
    meeting_id: str
    sender: str
    text: str