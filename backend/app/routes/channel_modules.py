from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.channel_modules import ChannelModule

router = APIRouter(prefix="/channel-modules", tags=["ChannelModules"])

@router.post("/", response_model=dict, status_code=201)
def assign_module_to_channel(
    channel_id: int,
    module_id: int,
    db: Session = Depends(get_db),
):
    from app.models.channel_modules import ChannelModule
    from app.models.module import Module
    
    # Validate module exists
    module = db.query(Module).filter(Module.module_id == module_id).first()
    if not module:
        raise HTTPException(status_code=404, detail="Module not found")
    
    # Check if already assigned
    existing = db.query(ChannelModule).filter(
        ChannelModule.channel_id == channel_id,
        ChannelModule.module_id == module_id
    ).first()
    if existing:
        return {"message": "Module already assigned to channel"}
    
    new_assignment = ChannelModule(
        channel_id=channel_id,
        module_id=module_id,
    )
    db.add(new_assignment)
    db.commit()
    db.refresh(new_assignment)
    return {"message": "Module assigned to channel", "assignment_id": new_assignment.assignment_id}

@router.get("/channel/{channel_id}", response_model=list)
def get_modules_by_channel(
    channel_id: int,
    db: Session = Depends(get_db),
):
    from app.models.channel_modules import ChannelModule
    assignments = db.query(ChannelModule).filter(ChannelModule.channel_id == channel_id).all()
    return [{"module_id": a.module_id} for a in assignments]