"""Compatibility wrapper for the channel management router.

The canonical HTTP layer now lives in ``app.routes.channel`` so the active
FastAPI application and any legacy ``routes.channel`` imports share the same
implementation and cannot drift apart.
"""

from app.routes.channel import router

__all__ = ["router"]
