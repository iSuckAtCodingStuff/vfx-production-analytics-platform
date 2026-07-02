"""
Database connection utilities for the VFX Production Analytics Platform.
"""

from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.engine import Engine
from sqlalchemy.engine import URL

from pipeline.config import DB_CONFIG

_engine: Engine | None = None


def get_engine() -> Engine:
    """Return a singleton SQLAlchemy engine"""

    global _engine

    if _engine is None:
      
        connection_url = URL.create(
            drivername="postgresql+psycopg2",
            username=DB_CONFIG["user"],
            password=DB_CONFIG["password"],
            host=DB_CONFIG["host"],
            port=DB_CONFIG["port"],
            database=DB_CONFIG["database"],
        )

        _engine = create_engine(connection_url, pool_pre_ping=True, future=True,)

    return _engine


def test_connection() -> bool:
    """Test database connectivity.
    Returns
    -------
    bool
        True if the connection succeeds"""

    try:
        engine = get_engine()

        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))

        return True

    except SQLAlchemyError:
        return False


def dispose_engine() -> None:
    """Dispose of the SQLAlchemy engine"""

    global _engine

    if _engine is not None:
        _engine.dispose()
        _engine = None
