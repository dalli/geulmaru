"""RSS feed fetching service."""
import logging
import time
import requests
from typing import Optional

from src.config import get_user_agent

logger = logging.getLogger(__name__)


def fetch_rss(feed_url: str, max_retries: int = 3, retry_delay: int = 2) -> Optional[str]:
    """Fetch RSS feed XML from a URL with retry logic.
    
    Args:
        feed_url: URL of the RSS feed
        max_retries: Maximum number of retry attempts (default: 3)
        retry_delay: Delay between retries in seconds (default: 2)
        
    Returns:
        RSS XML content as string, or None if fetch fails after all retries
        
    Raises:
        requests.RequestException: For network errors (handled internally)
    """
    headers = {
        "User-Agent": get_user_agent()
    }
    
    for attempt in range(max_retries):
        try:
            if attempt > 0:
                logger.info(f"Retry attempt {attempt}/{max_retries - 1} for RSS feed: {feed_url}")
            else:
                logger.info(f"Fetching RSS feed: {feed_url}")
            
            response = requests.get(feed_url, headers=headers, timeout=30)
            
            if response.status_code == 200:
                logger.info(f"Successfully fetched RSS feed: {feed_url}")
                return response.text
            else:
                logger.warning(f"Failed to fetch RSS feed. Status code: {response.status_code}, URL: {feed_url}")
                if attempt < max_retries - 1:
                    time.sleep(retry_delay)
                    continue
                return None
                
        except requests.Timeout:
            logger.warning(f"Timeout while fetching RSS feed: {feed_url}")
            if attempt < max_retries - 1:
                logger.info(f"Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
                continue
            logger.error(f"All retry attempts exhausted for RSS feed: {feed_url}")
            return None
            
        except requests.ConnectionError as e:
            logger.warning(f"Connection error while fetching RSS feed: {feed_url}, Error: {e}")
            if attempt < max_retries - 1:
                logger.info(f"Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
                continue
            logger.error(f"All retry attempts exhausted for RSS feed: {feed_url}")
            return None
            
        except requests.RequestException as e:
            logger.error(f"Network error while fetching RSS feed: {feed_url}, Error: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error while fetching RSS feed: {feed_url}, Error: {e}")
            return None
    
    logger.error(f"All retry attempts exhausted for RSS feed: {feed_url}")
    return None

