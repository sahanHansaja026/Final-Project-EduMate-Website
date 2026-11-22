"""Compatibility wrapper for the authorized-student router.

The canonical HTTP layer now lives in ``app.routes.authorized_students``.
"""

from app.routes.authorized_students import router

__all__ = ["router"]
