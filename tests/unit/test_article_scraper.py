"""Unit tests for Article Scraper service."""
import pytest
from unittest.mock import Mock, patch, MagicMock

# Import the service to be tested
from src.services import article_scraper


class TestArticleScraper:
    """Test cases for Article Scraper service."""
    
    def test_scrape_article_success(self):
        """Test successful article scraping."""
        article_url = "https://example.com/article/1"
        
        # Mock the newspaper Article class
        mock_article = Mock()
        mock_article.title = "Test Article"
        mock_article.authors = ["John Doe"]
        mock_article.text = "This is the article body."
        mock_article.images = ["https://example.com/image1.jpg"]
        mock_article.config = Mock()  # Add config attribute
        mock_article.download = Mock()
        mock_article.parse = Mock()
        
        # Patch at the module level where Article is used
        with patch('src.services.article_scraper.Article', return_value=mock_article):
            result = article_scraper.scrape_article(article_url)
            
            assert result is not None
            assert result['title'] == "Test Article"
            assert result['author'] == "John Doe"
            assert result['body'] == "This is the article body."
            assert len(result['media_links']) == 1
    
    def test_scrape_article_failure(self):
        """Test handling of scraping failures."""
        article_url = "https://example.com/article/1"
        
        with patch('newspaper.Article', side_effect=Exception("Scraping error")):
            result = article_scraper.scrape_article(article_url)
            assert result is None
    
    def test_scrape_article_no_content(self):
        """Test handling of articles with no content."""
        article_url = "https://example.com/article/1"
        
        mock_article = Mock()
        mock_article.title = "Test Article"
        mock_article.authors = []
        mock_article.text = ""
        mock_article.images = []
        mock_article.config = Mock()  # Add config attribute
        mock_article.download = Mock()
        mock_article.parse = Mock()
        
        with patch('src.services.article_scraper.Article', return_value=mock_article):
            result = article_scraper.scrape_article(article_url)
            
            assert result is not None
            assert result['title'] == "Test Article"
            assert result['author'] is None
            assert result['body'] == ""
            assert result['media_links'] == []

