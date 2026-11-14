"""Compatibility alias for the user comment model.

This module used to declare a second ``user_comments`` table, which made
SQLAlchemy raise ``Table 'user_comments' is already defined`` as soon as both
this module and ``app.models.user_comments`` were imported. ``UserComment`` is
the canonical definition, so re-export it under the historical ``Comment``
name instead of redefining the table.
"""

from app.models.user_comments import UserComment as Comment

__all__ = ["Comment"]
