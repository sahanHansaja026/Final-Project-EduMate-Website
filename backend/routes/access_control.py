from datetime import datetime
from models.subscription import PlanEnum


PLAN_ACCESS = {
    "free": {
        "content": ["home", "quiz", "basic_content"]
    },
    "premium": {
        "content": ["home", "quiz", "basic_content", "premium_content"]
    },
    "edu": {
        "content": ["home", "quiz", "basic_content", "premium_content", "edu_tools"]
    }
}


def is_subscription_active(sub):
    if not sub:
        return False

    now = datetime.utcnow()

    return (
        sub.start_date <= now and
        sub.end_date >= now and
        sub.status == "active"
    )


def can_access(sub, resource_type: str, resource_name: str) -> bool:
    if not is_subscription_active(sub):
        return False

    plan = sub.plan_name.value if hasattr(sub.plan_name, "value") else sub.plan_name

    if plan not in PLAN_ACCESS:
        return False

    return resource_name in PLAN_ACCESS[plan].get(resource_type, [])