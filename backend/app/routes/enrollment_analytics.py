from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.enrollment_analytics import EnrollmentAnalytics

router = APIRouter(prefix="/enrollment-analytics", tags=["EnrollmentAnalytics"])

@router.get("/overview", response_model=dict)
def get_enrollment_overview(
    db: Session = Depends(get_db),
):
    analytics = db.query(EnrollmentAnalytics).all()
    total_users = sum(a.total_users for a in analytics)
    total_enrollments = sum(a.total_enrollments for a in analytics)
    return {
        "total_users": total_users,
        "total_enrollments": total_enrollments,
    }

@router.get("/module/{module_id}", response_model=dict)
def get_module_analytics(
    module_id: int,
    db: Session = Depends(get_db),
):
    analytics = db.query(EnrollmentAnalytics).filter(EnrollmentAnalytics.module_id == module_id).first()
    if not analytics:
        return {"enrollments": 0, "completion_rate": 0}
    return {
        "enrollments": analytics.enrollments,
        "completion_rate": analytics.completion_rate,
    }