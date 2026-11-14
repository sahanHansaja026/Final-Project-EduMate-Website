from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.channel_analytics import ChannelAnalytics

router = APIRouter(prefix="/channel-analytics", tags=["ChannelAnalytics"])

@router.get("/overview", response_model=dict)
def get_channel_analytics_overview(
    db: Session = Depends(get_db),
):
    from app.models.channel_analytics import ChannelAnalytics
    analytics = db.query(ChannelAnalytics).all()
    total_channels = len(analytics)
    return {
        "total_channels": total_channels,
    }

@router.get("/channel/{channel_id}", response_model=dict)
def get_channel_analytics(
    channel_id: int,
    db: Session = Depends(get_db),
):
    from app.models.channel_analytics import ChannelAnalytics
    analytics = db.query(ChannelAnalytics).filter(ChannelAnalytics.channel_id == channel_id).first()
    if not analytics:
        return {"total_students": 0, "total_modules": 0, "total_enrollments": 0}
    return {
        "total_students": analytics.total_students,
        "total_modules": analytics.total_modules,
        "total_enrollments": analytics.total_enrollments,
    }