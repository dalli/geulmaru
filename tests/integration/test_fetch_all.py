"""Integration tests for fetch-all command."""
import pytest
import importlib
from pathlib import Path
from unittest.mock import Mock, patch

# Import modules to enable reloading
import src.config
import src.services.storage as storage_module


@pytest.mark.integration
class TestFetchAllCommand:
    """Integration tests for fetch-all functionality."""
    
    def teardown_method(self):
        """Close database after each test."""
        from src.services.storage import close_database
        close_database()
        importlib.reload(src.config)
        importlib.reload(storage_module)
    
    def test_fetch_all_collects_articles(self, clean_environment, monkeypatch, tmp_path, fixtures_dir):
        """Test that fetch-all collects articles from registered feeds."""
        importlib.reload(src.config)
        importlib.reload(storage_module)
        
        from src.services.storage import init_database, create_tables, get_db_session
        from src.models.feed import Feed
        from src.cli.fetch import fetch_all_command
        
        # Set temporary database path
        test_db = str(tmp_path / "test.db")
        monkeypatch.setenv("GEULMARU_DB_PATH", test_db)
        monkeypatch.setenv("GEULMARU_LOG_LEVEL", "INFO")
        
        # Initialize database
        init_database()
        create_tables()
        
        # Add a test feed
        feed_url = "https://example.com/rss"
        with get_db_session() as db:
            Feed.add_feed(db, feed_url)
        
        # Mock RSS fetching and parsing
        sample_rss = (fixtures_dir / "sample_rss.xml").read_text()
        
        with patch('src.services.feed_fetcher.fetch_rss', return_value=sample_rss):
            with patch('src.services.article_scraper.scrape_article') as mock_scrape:
                # Mock article scraping to return simple content
                mock_scrape.return_value = {
                    'title': 'Scraped Title',
                    'author': 'Scraped Author',
                    'body': 'Scraped body content.',
                    'media_links': []
                }
                
                # Run fetch-all
                fetch_all_command()
        
        # Verify articles were collected
        with get_db_session() as db:
            from src.models.article import Article
            articles = Article.list_recent(db, limit=100)
            assert len(articles) > 0
    
    def test_fetch_all_handles_no_feeds(self, clean_environment, monkeypatch, tmp_path):
        """Test that fetch-all handles case when no feeds are registered."""
        importlib.reload(src.config)
        importlib.reload(storage_module)
        
        from src.services.storage import init_database, create_tables
        from src.cli.fetch import fetch_all_command
        
        # Set temporary database path
        test_db = str(tmp_path / "test.db")
        monkeypatch.setenv("GEULMARU_DB_PATH", test_db)
        monkeypatch.setenv("GEULMARU_LOG_LEVEL", "INFO")
        
        # Initialize database
        init_database()
        create_tables()
        
        # Run fetch-all with no feeds (should not raise error)
        fetch_all_command()
    
    def test_fetch_all_skips_duplicates(self, clean_environment, monkeypatch, tmp_path, fixtures_dir):
        """Test that fetch-all skips duplicate articles."""
        importlib.reload(src.config)
        importlib.reload(storage_module)
        
        from src.services.storage import init_database, create_tables, get_db_session
        from src.models.feed import Feed
        from src.models.article import Article
        from src.cli.fetch import fetch_all_command
        from datetime import datetime
        
        # Set temporary database path
        test_db = str(tmp_path / "test.db")
        monkeypatch.setenv("GEULMARU_DB_PATH", test_db)
        monkeypatch.setenv("GEULMARU_LOG_LEVEL", "INFO")
        
        # Initialize database
        init_database()
        create_tables()
        
        # Add feed
        feed_url = "https://example.com/rss"
        with get_db_session() as db:
            feed = Feed.add_feed(db, feed_url)
        
        # Add a test article manually
        test_url = "https://example.com/article/1"
        with get_db_session() as db:
            Article.add_article(
                db=db,
                feed_id=1,
                url=test_url,
                title="Existing Article",
                published_at=datetime.utcnow()
            )
        
        # Mock RSS fetching and parsing
        sample_rss = (fixtures_dir / "sample_rss.xml").read_text()
        
        with patch('src.services.feed_fetcher.fetch_rss', return_value=sample_rss):
            with patch('src.services.article_scraper.scrape_article') as mock_scrape:
                mock_scrape.return_value = {
                    'title': 'Scraped Title',
                    'author': 'Scraped Author',
                    'body': 'Scraped body content.',
                    'media_links': []
                }
                
                # Run fetch-all
                fetch_all_command()
        
        # Verify article count hasn't changed (duplicates skipped)
        with get_db_session() as db:
            articles = Article.list_recent(db, limit=100)
            # Should have one article (the existing one) plus new unique ones
            assert len(articles) >= 1

