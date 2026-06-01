from datetime import datetime
from models.subscription import PlanEnum
from models.video import Video


def is_subscription_active(sub):
    if not sub:
        return False

    now = datetime.utcnow()

    return (
        sub.start_date <= now and
        sub.end_date >= now and
        sub.status == "active"
    )


# =========================
# VIDEO CREATION RULES
# =========================

def can_create_video(sub, db, user_id: int) -> bool:
    """
    Free plan → only 1 video
    Premium/Edu → unlimited
    """

    if not is_subscription_active(sub):
        return False

    plan = sub.plan_name.value if hasattr(sub.plan_name, "value") else sub.plan_name

    # 🔥 FREE PLAN RULE
    if plan == "free":
        video_count = db.query(Video).filter(
            Video.user_id == user_id
        ).count()

        return video_count < 1

    # 🔥 PREMIUM / EDU → unlimited
    return True


# =========================
# OPTIONAL: VIDEO ACCESS VIEW RULES
# =========================

def can_view_video(sub, resource_name: str) -> bool:
    """
    Example: reuse your PLAN_ACCESS idea
    """

    if not is_subscription_active(sub):
        return False

    plan = sub.plan_name.value if hasattr(sub.plan_name, "value") else sub.plan_name

    PLAN_ACCESS = {
        "free": ["home", "quiz"],
        "premium": ["home", "quiz", "premium_content", "video"],
        "edu": ["home", "quiz", "premium_content", "edu_tools", "video"]
    }

    return resource_name in PLAN_ACCESS.get(plan, [])