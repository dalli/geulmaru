"""Unit tests for Feed Fetcher service."""
import pytest
import requests
from unittest.mock import Mock, patch

# Import the service to be tested
from src.services import feed_fetcher


class TestFeedFetcher:
    """Test cases for Feed Fetcher service."""
    
    def test_fetch_rss_from_url_success(self):
        """Test successful RSS fetching from URL."""
        # This test will fail initially until implementation
        feed_url = "https://example.com/rss"
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = '<?xml version="1.0"?><rss><channel></channel></rss>'
        
        with patch('requests.get', return_value=mock_response):
            result = feed_fetcher.fetch_rss(feed_url)
            assert result == mock_response.text
    
    def test_fetch_rss_network_failure(self):
        """Test handling of network failures."""
        feed_url = "https://example.com/rss"
        
        with patch('requests.get', side_effect=requests.RequestException("Network error")):
            result = feed_fetcher.fetch_rss(feed_url)
            assert result is None
    
    def test_fetch_rss_invalid_status_code(self):
        """Test handling of non-200 status codes."""
        feed_url = "https://example.com/rss"
        mock_response = Mock()
        mock_response.status_code = 404
        
        with patch('requests.get', return_value=mock_response):
            result = feed_fetcher.fetch_rss(feed_url)
            assert result is None
    
    def test_fetch_rss_timeout(self):
        """Test handling of timeout errors."""
        feed_url = "https://example.com/rss"
        
        with patch('requests.get', side_effect=requests.Timeout("Timeout")):
            result = feed_fetcher.fetch_rss(feed_url)
            assert result is None

