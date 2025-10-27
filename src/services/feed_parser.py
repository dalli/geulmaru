"""RSS feed parsing service."""
import logging
import feedparser
from datetime import datetime
from typing import List, Dict, Any, Optional

logger = logging.getLogger(__name__)


def parse_rss(rss_content: str) -> List[Dict[str, Any]]:
    """Parse RSS XML content and extract article metadata.
    
    Args:
        rss_content: Raw RSS XML content as string
        
    Returns:
        List of article dictionaries with metadata:
        - url: Article URL (required)
        - title: Article title (required)
        - published_at: Publication datetime (optional)
        - author: Author name (optional)
    """
    articles = []
    
    try:
        feed = feedparser.parse(rss_content)
        
        if feed.bozo and feed.bozo_exception:
            logger.warning(f"RSS parsing encountered issue: {feed.bozo_exception}")
        
        for entry in feed.entries:
            # Extract article metadata
            article_data = {
                'url': entry.get('link') or entry.get('id'),
                'title': entry.get('title', 'Untitled'),
                'published_at': _parse_date(entry.get('published') or entry.get('updated')),
                'author': _extract_author(entry.get('author')),
            }
            
            # Only add if we have a valid URL
            if article_data['url']:
                articles.append(article_data)
                logger.debug(f"Parsed article: {article_data['title'][:50]}")
            else:
                logger.warning("Skipping article entry without URL")
        
        logger.info(f"Parsed {len(articles)} articles from RSS feed")
        
    except Exception as e:
        logger.error(f"Error parsing RSS content: {e}")
    
    return articles


def _parse_date(date_str: Optional[str]) -> Optional[datetime]:
    """Parse date string to datetime object.
    
    Args:
        date_str: Date string in various formats
        
    Returns:
        datetime object or None if parsing fails
    """
    if not date_str:
        return None
    
    try:
        # Try common date formats
        parsed = feedparser._parse_date(date_str)
        if parsed:
            return parsed
    except:
        pass
    
    # Try manual parsing with common formats
    date_formats = [
        "%a, %d %b %Y %H:%M:%S %z",  # RFC 2822
        "%a, %d %b %Y %H:%M:%S %Z",  # RFC 2822 with timezone name
        "%Y-%m-%dT%H:%M:%S%z",       # ISO 8601
    ]
    
    for fmt in date_formats:
        try:
            return datetime.strptime(date_str, fmt)
        except:
            continue
    
    logger.warning(f"Could not parse date string: {date_str}")
    return None


def _extract_author(author_str: Optional[str]) -> Optional[str]:
    """Extract author name from various formats.
    
    Args:
        author_str: Author string (may include email, etc.)
        
    Returns:
        Clean author name or None
    """
    if not author_str:
        return None
    
    # Common format: "email@example.com (Name)" or just "Name"
    if '(' in author_str and ')' in author_str:
        start = author_str.rfind('(') + 1
        end = author_str.rfind(')')
        return author_str[start:end].strip()
    
    # If it looks like an email, return None
    if '@' in author_str:
        return None
    
    return author_str.strip()

