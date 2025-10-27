"""RSS feed fetching service."""
import logging
import requests
from typing import Optional

from src.config import get_user_agent

logger = logging.getLogger(__name__)


def fetch_rss(feed_url: str) -> Optional[str]:
    """Fetch RSS feed XML from a URL.
    
    Args:
        feed_url: URL of the RSS feed
        
    Returns:
        RSS XML content as string, or None if fetch fails
        
    Raises:
        requests.RequestException: For network errors (handled internally)
    """
    try:
        logger.info(f"Fetching RSS feed: {feed_url}")
        
        headers = {
            "User-Agent": get_user_agent()
        }
        
        response = requests.get(feed_url, headers=headers, timeout=30)
        
        if response.status_code == 200:
            logger.info(f"Successfully fetched RSS feed: {feed_url}")
            return response.text
        else:
            logger.error(f"Failed to fetch RSS feed. Status code: {response.status_code}, URL: {feed_url}")
            return None
            
    except requests.Timeout:
        logger.error(f"Timeout while fetching RSS feed: {feed_url}")
        return None
    except requests.RequestException as e:
        logger.error(f"Network error while fetching RSS feed: {feed_url}, Error: {e}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error while fetching RSS feed: {feed_url}, Error: {e}")
        return None

