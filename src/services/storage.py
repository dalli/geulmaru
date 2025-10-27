"""Database storage and initialization service."""
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from contextlib import contextmanager

from src.config import GEULMARU_DB_PATH
from src.models.feed import Feed, Base
from src.models.article import Article, Base as ArticleBase

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
    
    # Create database engine
    db_url = f"sqlite:///{GEULMARU_DB_PATH}"
    _engine = create_engine(db_url, echo=False)
    
    # Create session factory
    _SessionLocal = sessionmaker(bind=_engine)
    
    logger.info(f"Database initialized: {GEULMARU_DB_PATH}")


def create_tables() -> None:
    """Create all database tables if they don't exist."""
    if _engine is None:
        raise RuntimeError("Database not initialized. Call init_database() first.")
    
    # Import all models to ensure they're registered with SQLAlchemy
    from src.models.feed import Feed
    from src.models.article import Article
    
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
    return os.path.exists(GEULMARU_DB_PATH)


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

