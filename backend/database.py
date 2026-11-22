"""Backward-compatible re-exports for the centralized database module.

Database configuration and connection management now live in
:mod:`app.core.database`. This module only re-exports the shared objects so
that pre-existing imports keep working; new code should import from
:mod:`app.core.database` directly.
"""

from app.core.database import Base, SessionLocal, engine, get_db  # noqa: F401

__all__ = ["Base", "SessionLocal", "engine", "get_db"]
