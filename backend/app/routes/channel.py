from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.channel import Channel

router = APIRouter(prefix="/channels", tags=["Channels"])

@router.post("/", response_model=dict, status_code=201)
def create_channel(
    name: str,
    description: str = None,
    is_private: bool = False,
    db: Session = Depends(get_db),
):
    from app.models.channel import Channel
    new_channel = Channel(
        name=name,
        description=description,
        is_private=is_private,
    )
    db.add(new_channel)
    db.commit()
    db.refresh(new_channel)
    return {"message": "Channel created", "channel_id": new_channel.channel_id}

@router.get("/", response_model=list)
def get_channels(
    db: Session = Depends(get_db),
    is_private: bool = None,
):
    query = db.query(Channel)
    if is_private is not None:
        query = query.filter(Channel.is_private == is_private)
    return query.all()

@router.get("/{channel_id}", response_model=dict)
def get_channel(
    channel_id: int,
    db: Session = Depends(get_db),
):
    from app.models.channel import Channel
    channel = db.query(Channel).filter(Channel.channel_id == channel_id).first()
    if not channel:
        raise HTTPException(status_code=404, detail="Channel not found")
    return {
        "channel_id": channel.channel_id,
        "name": channel.name,
        "description": channel.description,
        "is_private": channel.is_private,
    }