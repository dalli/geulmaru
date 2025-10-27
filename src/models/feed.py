"""Feed model for RSS feed management."""
import logging
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Index
from sqlalchemy.orm import Session

from src.models import Base

logger = logging.getLogger(__name__)


class Feed(Base):
    """Represents a registered RSS feed URL."""
    
    __tablename__ = "feeds"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    url = Column(String, unique=True, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    
    __table_args__ = (
        Index("idx_feeds_url", "url"),
    )
    
    def __repr__(self) -> str:
        return f"<Feed(id={self.id}, url='{self.url}', created_at='{self.created_at}')>"
    
    @staticmethod
    def add_feed(db: Session, url: str) -> "Feed":
        """Add a new RSS feed to the database.
        
        Args:
            db: Database session
            url: RSS feed URL to add
            
        Returns:
            Feed instance that was added
            
        Raises:
            ValueError: If URL is invalid or already exists
        """
        from urllib.parse import urlparse
        
        # Validate URL
        parsed = urlparse(url)
        if not parsed.scheme or not parsed.netloc:
            logger.error(f"Invalid URL format: {url}")
            raise ValueError(f"Invalid URL format: {url}")
        
        if parsed.scheme not in ["http", "https"]:
            logger.error(f"URL must use HTTP or HTTPS protocol: {url}")
            raise ValueError(f"URL must use HTTP or HTTPS protocol: {url}")
        
        # Check for duplicates
        existing_feed = db.query(Feed).filter(Feed.url == url).first()
        if existing_feed:
            logger.warning(f"Attempt to add duplicate feed: {url}")
            raise ValueError(f"Feed URL already exists: {url}")
        
        # Create new feed
        feed = Feed(url=url, created_at=datetime.utcnow())
        db.add(feed)
        db.commit()
        db.refresh(feed)
        
        logger.debug(f"Created feed: ID={feed.id}, URL={url}")
        return feed
    
    @staticmethod
    def list_all(db: Session) -> list["Feed"]:
        """List all registered feeds.
        
        Args:
            db: Database session
            
        Returns:
            List of all Feed instances, ordered by created_at descending
        """
        return db.query(Feed).order_by(Feed.created_at.desc()).all()
    
    @staticmethod
    def get_by_id(db: Session, feed_id: int) -> "Feed":
        """Get feed by ID.
        
        Args:
            db: Database session
            feed_id: Feed ID to look up
            
        Returns:
            Feed instance or None if not found
        """
        return db.query(Feed).filter(Feed.id == feed_id).first()
    
    @staticmethod
    def remove_feed(db: Session, feed_id: int) -> bool:
        """Remove a feed from the database.
        
        Args:
            db: Database session
            feed_id: Feed ID to remove
            
        Returns:
            True if removed, False if not found
        """
        feed = Feed.get_by_id(db, feed_id)
        if not feed:
            return False
        
        db.delete(feed)
        db.commit()
        return True

