from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.channel import Channel

router = APIRouter(prefix="/student-enrollment-count-channel", tags=["StudentEnrollmentCountChannel"])

@router.get("/channel/{channel_id}", response_model=dict)
def get_student_enrollment_count(
    channel_id: int,
    db: Session = Depends(get_db),
):
    from app.models.enrollment import Enrollment
    from app.models.channel_modules import ChannelModule
    
    # Get all modules in the channel
    channel_modules = db.query(ChannelModule).filter(ChannelModule.channel_id == channel_id).all()
    module_ids = [cm.module_id for cm in channel_modules]
    
    # Count enrollments for each module
    total_enrollments = 0
    for module_id in module_ids:
        count = db.query(Enrollment).filter(Enrollment.module_id == module_id).count()
        total_enrollments += count
    
    return {
        "channel_id": channel_id,
        "total_modules": len(module_ids),
        "total_student_enrollments": total_enrollments,
    }