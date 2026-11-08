from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.channel_content_access_controller import ChannelContentAccessController

router = APIRouter(prefix="/channel-content-access", tags=["ChannelContentAccess"])

@router.post("/grant", response_model=dict)
def grant_content_access(
    channel_id: int,
    content_id: int,
    user_id: int,
    db: Session = Depends(get_db),
):
    from app.models.channel_content_access_controller import ChannelContentAccessController
    # Check if already granted
    existing = db.query(ChannelContentAccessController).filter(
        ChannelContentAccessController.channel_id == channel_id,
        ChannelContentAccessController.content_id == content_id,
        ChannelContentAccessController.user_id == user_id
    ).first()
    if existing:
        return {"message": "Content access already granted"}
    
    new_access = ChannelContentAccessController(
        channel_id=channel_id,
        content_id=content_id,
        user_id=user_id,
    )
    db.add(new_access)
    db.commit()
    return {"message": "Content access granted"}

@router.post("/revoke", response_model=dict)
def revoke_content_access(
    channel_id: int,
    content_id: int,
    user_id: int,
    db: Session = Depends(get_db),
):
    from app.models.channel_content_access_controller import ChannelContentAccessController
    access = db.query(ChannelContentAccessController).filter(
        ChannelContentAccessController.channel_id == channel_id,
        ChannelContentAccessController.content_id == content_id,
        ChannelContentAccessController.user_id == user_id
    ).first()
    if not access:
        raise HTTPException(status_code=404, detail="Access not found")
    
    db.delete(access)
    db.commit()
    return {"message": "Content access revoked"}

@router.get("/channel/{channel_id}/content/{content_id}", response_model=bool)
def check_content_access(
    channel_id: int,
    content_id: int,
    user_id: int,
    db: Session = Depends(get_db),
):
    from app.models.channel_content_access_controller import ChannelContentAccessController
    access = db.query(ChannelContentAccessController).filter(
        ChannelContentAccessController.channel_id == channel_id,
        ChannelContentAccessController.content_id == content_id,
        ChannelContentAccessController.user_id == user_id
    ).first()
    return {"has_access": access is not None}