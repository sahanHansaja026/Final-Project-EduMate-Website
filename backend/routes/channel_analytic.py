"""Compatibility wrapper for the channel analytics router.

The canonical HTTP layer now lives in ``app.routes.channel_analytic``.
"""

from app.routes.channel_analytic import router

__all__ = ["router"]
