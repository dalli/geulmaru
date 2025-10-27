"""Models for Geulmaru RSS Collector."""
from sqlalchemy.ext.declarative import declarative_base

# Shared Base for all models
Base = declarative_base()

# Import models to register them with SQLAlchemy
from src.models.feed import Feed  # noqa: E402
from src.models.article import Article  # noqa: E402

__all__ = ["Base", "Feed", "Article"]
