"""Configuration and environment settings for Geulmaru application."""
import os
import logging
from pathlib import Path
from typing import Optional


# Environment variables - get fresh values on each access
def get_db_path() -> str:
    """Get database path from environment variable."""
    return os.getenv("GEULMARU_DB_PATH", "./geulmaru.db")


def get_log_level_env() -> str:
    """Get log level from environment variable."""
    return os.getenv("GEULMARU_LOG_LEVEL", "INFO")


def get_user_agent() -> str:
    """Get user agent from environment variable."""
    return os.getenv(
        "GEULMARU_USER_AGENT",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    )


# Backward compatibility
GEULMARU_DB_PATH = get_db_path()
GEULMARU_LOG_LEVEL = get_log_level_env()
GEULMARU_USER_AGENT = get_user_agent()


def get_log_level() -> int:
    """Convert string log level to logging constant."""
    level_mapping = {
        "DEBUG": logging.DEBUG,
        "INFO": logging.INFO,
        "WARNING": logging.WARNING,
        "ERROR": logging.ERROR,
        "CRITICAL": logging.CRITICAL,
    }
    return level_mapping.get(get_log_level_env().upper(), logging.INFO)


def setup_logging() -> None:
    """Configure structured logging with levels and context.
    
    Provides structured logging with:
    - Timestamp
    - Module name
    - Log level
    - Contextual message
    - Support for additional context fields
    """
    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    date_format = "%Y-%m-%d %H:%M:%S"
    
    # Get environment-based log level
    log_level = get_log_level()
    
    logging.basicConfig(
        level=log_level,
        format=log_format,
        datefmt=date_format,
        handlers=[
            logging.StreamHandler()  # Use stream handler for better compatibility
        ]
    )
    
    # Set level for root logger to avoid double messages
    logging.getLogger().setLevel(log_level)
    
    # Disable noisy third-party loggers
    logging.getLogger("newspaper").setLevel(logging.WARNING)
    logging.getLogger("requests").setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("sqlalchemy").setLevel(logging.WARNING)
    
    # Create logger for the application
    logger = logging.getLogger("geulmaru")
    logger.info(f"Logging initialized with level: {get_log_level_env()}")


def validate_db_path() -> bool:
    """Validate database file path and parent directory permissions."""
    db_path = Path(get_db_path())
    parent_dir = db_path.parent
    
    # Check if parent directory exists and is writable
    if not parent_dir.exists():
        try:
            parent_dir.mkdir(parents=True, exist_ok=True)
        except (PermissionError, OSError) as e:
            logging.error(f"Cannot create database directory: {e}")
            return False
    
    # Check if we can write to the parent directory
    if not os.access(parent_dir, os.W_OK):
        logging.error(f"Cannot write to database directory: {parent_dir}")
        return False
    
    return True

