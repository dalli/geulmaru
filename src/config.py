"""Configuration and environment settings for Geulmaru application."""
import os
import logging
from pathlib import Path
from typing import Optional


# Environment variables
GEULMARU_DB_PATH = os.getenv("GEULMARU_DB_PATH", "./geulmaru.db")
GEULMARU_LOG_LEVEL = os.getenv("GEULMARU_LOG_LEVEL", "INFO")
GEULMARU_USER_AGENT = os.getenv(
    "GEULMARU_USER_AGENT",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
)


def get_log_level() -> int:
    """Convert string log level to logging constant."""
    level_mapping = {
        "DEBUG": logging.DEBUG,
        "INFO": logging.INFO,
        "WARNING": logging.WARNING,
        "ERROR": logging.ERROR,
        "CRITICAL": logging.CRITICAL,
    }
    return level_mapping.get(GEULMARU_LOG_LEVEL.upper(), logging.INFO)


def setup_logging() -> None:
    """Configure structured logging with levels."""
    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    date_format = "%Y-%m-%d %H:%M:%S"
    
    logging.basicConfig(
        level=get_log_level(),
        format=log_format,
        datefmt=date_format,
    )
    
    # Create logger for the application
    logger = logging.getLogger("geulmaru")
    logger.info(f"Logging initialized with level: {GEULMARU_LOG_LEVEL}")


def validate_db_path() -> bool:
    """Validate database file path and parent directory permissions."""
    db_path = Path(GEULMARU_DB_PATH)
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

