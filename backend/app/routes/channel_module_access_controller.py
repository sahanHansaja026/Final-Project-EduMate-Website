from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.channel_module_access_controller import ChannelModuleAccessController

router = APIRouter(prefix="/channel-module-access", tags=["ChannelModuleAccess"])

@router.post("/grant", response_model=dict)
def grant_module_access(
    channel_id: int,
    module_id: int,
    user_id: int,
    db: Session = Depends(get_db),
):
    from app.models.channel_module_access_controller import ChannelModuleAccessController
    # Check if already granted
    existing = db.query(ChannelModuleAccessController).filter(
        ChannelModuleAccessController.channel_id == channel_id,
        ChannelModuleAccessController.module_id == module_id,
        ChannelModuleAccessController.user_id == user_id
    ).first()
    if existing:
        return {"message": "Access already granted"}
    
    new_access = ChannelModuleAccessController(
        channel_id=channel_id,
        module_id=module_id,
        user_id=user_id,
    )
    db.add(new_access)
    db.commit()
    return {"message": "Module access granted"}

@router.post("/revoke", response_model=dict)
def revoke_module_access(
    channel_id: int,
    module_id: int,
    user_id: int,
    db: Session = Depends(get_db),
):
    from app.models.channel_module_access_controller import ChannelModuleAccessController
    access = db.query(ChannelModuleAccessController).filter(
        ChannelModuleAccessController.channel_id == channel_id,
        ChannelModuleAccessController.module_id == module_id,
        ChannelModuleAccessController.user_id == user_id
    ).first()
    if not access:
        raise HTTPException(status_code=404, detail="Access not found")
    
    db.delete(access)
    db.commit()
    return {"message": "Module access revoked"}

@router.get("/channel/{channel_id}/module/{module_id}", response_model=bool)
def check_module_access(
    channel_id: int,
    module_id: int,
    user_id: int,
    db: Session = Depends(get_db),
):
    from app.models.channel_module_access_controller import ChannelModuleAccessController
    access = db.query(ChannelModuleAccessController).filter(
        ChannelModuleAccessController.channel_id == channel_id,
        ChannelModuleAccessController.module_id == module_id,
        ChannelModuleAccessController.user_id == user_id
    ).first()
    return {"has_access": access is not None}