"""Article scraping service for extracting content from URLs."""
import logging
from typing import Dict, Any, Optional
from newspaper import Article

from src.config import get_user_agent

logger = logging.getLogger(__name__)


def scrape_article(article_url: str) -> Optional[Dict[str, Any]]:
    """Scrape article content from a URL.
    
    Args:
        article_url: URL of the article to scrape
        
    Returns:
        Dictionary with scraped article data:
        - title: Article title
        - author: Author name (optional)
        - body: Full article body text
        - media_links: List of media URLs (images, videos)
        Returns None if scraping fails
    """
    try:
        logger.info(f"Scraping article: {article_url}")
        
        # Create article object
        article = Article(article_url)
        
        # Set user agent via configuration
        article.config.browser_user_agent = get_user_agent()
        
        # Download and parse
        article.download()
        article.parse()
        
        # Extract data
        scraped_data = {
            'title': article.title or 'Untitled',
            'author': article.authors[0] if article.authors else None,
            'body': article.text or '',
            'media_links': article.images or [],
        }
        
        logger.info(f"Successfully scraped article: {article_url}")
        logger.debug(f"Extracted: title='{scraped_data['title'][:50]}', "
                    f"author='{scraped_data['author']}', "
                    f"body_length={len(scraped_data['body'])}, "
                    f"media_count={len(scraped_data['media_links'])}")
        
        return scraped_data
        
    except Exception as e:
        logger.error(f"Failed to scrape article: {article_url}, Error: {e}")
        return None

