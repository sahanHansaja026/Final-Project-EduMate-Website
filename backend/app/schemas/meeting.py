from pydantic import BaseModel

class MeetingCreate(BaseModel):
    title: str
    host_id: str


class MeetingResponse(BaseModel):
    id: str
    title: str
    host_id: str

    class Config:
        from_attributes = True