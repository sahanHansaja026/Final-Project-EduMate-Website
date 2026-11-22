"""Centralized database engine, session and configuration management.

All database configuration and connection handling for the EduMate backend
lives here. The SQLAlchemy engine, the session factory and the FastAPI
``get_db`` dependency are created once from the environment based settings and
are reused across the application, so a single connection pool is shared
instead of creating engines per module.
"""

from typing import Iterator, Optional

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine, make_url
from sqlalchemy.orm import Session, declarative_base, sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.config import settings


def create_database_engine(database_url: Optional[str] = None, **engine_kwargs) -> Engine:
    """Create a SQLAlchemy engine for the given database URL.

    Connection pooling (with a pre-ping for liveness) and sensible pool sizing
    are enabled by default and can be tuned through the environment. In-memory
    SQLite databases (used by the test suite) get a static pool so that a single
    connection is shared across the process.
    """
    url = database_url if database_url is not None else settings.database_url
    engine_kwargs.setdefault("pool_pre_ping", True)
    engine_kwargs.setdefault("pool_recycle", settings.DB_POOL_RECYCLE_SECONDS)

    parsed_url = make_url(url)
    is_in_memory_sqlite = (
        parsed_url.get_backend_name() == "sqlite"
        and parsed_url.database in (None, "", ":memory:")
    )
    if is_in_memory_sqlite:
        engine_kwargs.setdefault("connect_args", {"check_same_thread": False})
        engine_kwargs.setdefault("poolclass", StaticPool)
    else:
        engine_kwargs.setdefault("pool_size", settings.DB_POOL_SIZE)
        engine_kwargs.setdefault("max_overflow", settings.DB_MAX_OVERFLOW)

    return create_engine(url, **engine_kwargs)


engine = create_database_engine()

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    expire_on_commit=False,
)

Base = declarative_base()


def init_db(bind_engine: Optional[Engine] = None) -> None:
    """Create the database tables registered on the shared declarative metadata."""
    Base.metadata.create_all(bind=bind_engine if bind_engine is not None else engine)


def get_db() -> Iterator[Session]:
    """FastAPI dependency that yields a database session.

    - The session is rolled back when the request handling fails, so failed
      operations never leave incomplete transactions behind.
    - The session is always closed afterwards, releasing the connection back
      to the pool.
    """
    db = SessionLocal()
    try:
        yield db
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()
