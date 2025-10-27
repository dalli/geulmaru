"""Database storage and initialization service."""
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from contextlib import contextmanager

from src.config import get_db_path
from src.models import Base, Feed, Article

logger = logging.getLogger(__name__)

# Database engine and session
_engine = None
_SessionLocal = None


def init_database() -> None:
    """Initialize database connection and create tables."""
    global _engine, _SessionLocal
    
    if _engine is not None:
        logger.warning("Database already initialized")
        return
    
    # Get fresh database path from environment
    db_path = get_db_path()
    
    # Ensure parent directory exists
    from pathlib import Path
    db_file = Path(db_path)
    db_file.parent.mkdir(parents=True, exist_ok=True)
    
    db_url = f"sqlite:///{db_path}"
    _engine = create_engine(db_url, echo=False)
    
    # Create session factory
    _SessionLocal = sessionmaker(bind=_engine)
    
    logger.info(f"Database initialized: {db_path}")


def create_tables() -> None:
    """Create all database tables if they don't exist."""
    if _engine is None:
        raise RuntimeError("Database not initialized. Call init_database() first.")
    
    # Create tables
    Base.metadata.create_all(_engine)
    logger.info("Database tables created successfully")


def get_session() -> Session:
    """Get a new database session.
    
    Returns:
        Database session
        
    Raises:
        RuntimeError: If database is not initialized
    """
    if _SessionLocal is None:
        raise RuntimeError("Database not initialized. Call init_database() first.")
    
    return _SessionLocal()


@contextmanager
def get_db_session():
    """Context manager for database sessions with automatic cleanup.
    
    Yields:
        Database session
        
    Example:
        with get_db_session() as db:
            feeds = Feed.list_all(db)
    """
    session = get_session()
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        logger.error(f"Database session error: {e}")
        raise
    finally:
        session.close()


def check_database_exists() -> bool:
    """Check if database file exists.
    
    Returns:
        True if database file exists, False otherwise
    """
    import os
    return os.path.exists(get_db_path())


def reset_database() -> None:
    """Reset database by dropping all tables and recreating them.
    
    WARNING: This will delete all data!
    """
    if _engine is None:
        raise RuntimeError("Database not initialized. Call init_database() first.")
    
    # Drop all tables
    Base.metadata.drop_all(_engine)
    logger.warning("All database tables dropped")
    
    # Recreate tables
    create_tables()
    logger.info("Database reset successfully")


def close_database() -> None:
    """Close database connection and reset global state.
    
    This is mainly for testing purposes to allow reinitialization.
    """
    global _engine, _SessionLocal
    
    if _engine is not None:
        _engine.dispose()
        logger.info("Database connection closed")
    
    _engine = None
    _SessionLocal = None

