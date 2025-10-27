"""Article model for scraped news articles."""
from datetime import datetime
from typing import Optional, List
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Index
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, relationship

Base = declarative_base()


class Article(Base):
    """Represents a scraped news article with full content."""
    
    __tablename__ = "articles"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    feed_id = Column(Integer, ForeignKey("feeds.id"), nullable=False)
    url = Column(String, unique=True, nullable=False)
    title = Column(String, nullable=False)
    author = Column(String, nullable=True)
    body = Column(Text, nullable=True)
    media_links = Column(Text, nullable=True)
    published_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    
    __table_args__ = (
        Index("idx_articles_feed_id", "feed_id"),
        Index("idx_articles_url", "url"),
        Index("idx_articles_published_at", "published_at"),
        Index("idx_articles_created_at", "created_at"),
    )
    
    def __repr__(self) -> str:
        return f"<Article(id={self.id}, title='{self.title[:30]}...', url='{self.url}')>"
    
    @staticmethod
    def add_article(
        db: Session,
        feed_id: int,
        url: str,
        title: str,
        author: Optional[str] = None,
        body: Optional[str] = None,
        media_links: Optional[str] = None,
        published_at: Optional[datetime] = None,
    ) -> "Article":
        """Add a new article to the database.
        
        Args:
            db: Database session
            feed_id: ID of the source RSS feed
            url: Article URL (must be unique)
            title: Article title
            author: Article author (optional)
            body: Full article body text (optional)
            media_links: Newline-separated media URLs (optional)
            published_at: Original publication timestamp (optional)
            
        Returns:
            Article instance that was added
            
        Raises:
            ValueError: If URL already exists
        """
        # Check for duplicates
        existing_article = db.query(Article).filter(Article.url == url).first()
        if existing_article:
            raise ValueError(f"Article URL already exists: {url}")
        
        article = Article(
            feed_id=feed_id,
            url=url,
            title=title,
            author=author,
            body=body,
            media_links=media_links,
            published_at=published_at,
            created_at=datetime.utcnow(),
        )
        db.add(article)
        db.commit()
        db.refresh(article)
        
        return article
    
    @staticmethod
    def list_recent(db: Session, limit: int = 10) -> List["Article"]:
        """List recent articles from the archive.
        
        Args:
            db: Database session
            limit: Maximum number of articles to return
            
        Returns:
            List of recent Article instances, ordered by created_at descending
        """
        return (
            db.query(Article)
            .order_by(Article.created_at.desc())
            .limit(limit)
            .all()
        )
    
    @staticmethod
    def search_by_keyword(db: Session, keyword: str, limit: int = 50) -> List["Article"]:
        """Search articles containing a keyword in title or body.
        
        Args:
            db: Database session
            keyword: Search keyword
            limit: Maximum number of results to return
            
        Returns:
            List of Article instances matching the keyword
        """
        return (
            db.query(Article)
            .filter(
                (Article.title.contains(keyword)) | (Article.body.contains(keyword))
            )
            .order_by(Article.created_at.desc())
            .limit(limit)
            .all()
        )
    
    @staticmethod
    def get_by_url(db: Session, url: str) -> Optional["Article"]:
        """Get article by URL.
        
        Args:
            db: Database session
            url: Article URL to look up
            
        Returns:
            Article instance or None if not found
        """
        return db.query(Article).filter(Article.url == url).first()
    
    @staticmethod
    def exists_by_url(db: Session, url: str) -> bool:
        """Check if article with given URL already exists.
        
        Args:
            db: Database session
            url: Article URL to check
            
        Returns:
            True if article exists, False otherwise
        """
        return db.query(Article).filter(Article.url == url).first() is not None

