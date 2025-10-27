"""Integration tests for feed add command."""
import pytest
import importlib
from pathlib import Path

# Import modules to enable reloading
import src.config
import src.services.storage as storage_module


@pytest.mark.integration
class TestFeedAddCommand:
    """Integration tests for feed add CLI command."""
    
    def teardown_method(self):
        """Close database after each test."""
        from src.services.storage import close_database
        close_database()
        importlib.reload(src.config)
        importlib.reload(storage_module)
    
    def test_feed_add_with_valid_url(self, clean_environment, monkeypatch, tmp_path):
        """Test feed add command with valid URL."""
        # Reload modules
        importlib.reload(src.config)
        importlib.reload(storage_module)
        
        # Set temporary database path
        test_db = str(tmp_path / "test.db")
        monkeypatch.setenv("GEULMARU_DB_PATH", test_db)
        
        from src.services.storage import init_database, create_tables
        from src.models.feed import Feed
        
        # Initialize database
        init_database()
        create_tables()
        
        from src.services.storage import get_session
        from src.models.feed import Feed
        
        # Test adding a feed
        url = "https://example.com/rss"
        session = get_session()
        try:
            feed = Feed.add_feed(session, url)
            assert feed is not None
            assert feed.url == url
            
            # Verify feed is in database
            retrieved = session.query(Feed).filter(Feed.url == url).first()
            assert retrieved is not None
            assert retrieved.url == url
        finally:
            session.close()
    
    def test_feed_add_with_invalid_url(self, clean_environment, monkeypatch, tmp_path):
        """Test feed add command with invalid URL."""
        # Reload modules
        importlib.reload(src.config)
        importlib.reload(storage_module)
        
        # Set temporary database path
        test_db = str(tmp_path / "test.db")
        monkeypatch.setenv("GEULMARU_DB_PATH", test_db)
        
        from src.services.storage import init_database, create_tables
        
        # Initialize database
        init_database()
        create_tables()
        
        from src.models.feed import Feed
        from src.services.storage import get_session
        
        session = get_session()
        try:
            # Test with invalid URL
            with pytest.raises(ValueError):
                Feed.add_feed(session, "invalid-url")
        finally:
            session.close()
    
    def test_feed_add_duplicate_url(self, clean_environment, monkeypatch, tmp_path):
        """Test feed add command with duplicate URL."""
        # Reload modules
        importlib.reload(src.config)
        importlib.reload(storage_module)
        
        # Set temporary database path
        test_db = str(tmp_path / "test.db")
        monkeypatch.setenv("GEULMARU_DB_PATH", test_db)
        
        from src.services.storage import init_database, create_tables
        
        # Initialize database
        init_database()
        create_tables()
        
        from src.models.feed import Feed
        from src.services.storage import get_session
        
        session = get_session()
        try:
            url = "https://example.com/rss"
            
            # Add first feed
            Feed.add_feed(session, url)
            
            # Try to add duplicate
            with pytest.raises(ValueError, match="already exists"):
                Feed.add_feed(session, url)
        finally:
            session.close()
    
    def test_feed_add_multiple_feeds(self, clean_environment, monkeypatch, tmp_path):
        """Test adding multiple feeds."""
        # Reload modules
        importlib.reload(src.config)
        importlib.reload(storage_module)
        
        # Set temporary database path
        test_db = str(tmp_path / "test.db")
        monkeypatch.setenv("GEULMARU_DB_PATH", test_db)
        
        from src.services.storage import init_database, create_tables
        
        # Initialize database
        init_database()
        create_tables()
        
        from src.models.feed import Feed
        from src.services.storage import get_session
        
        session = get_session()
        try:
            # Add multiple feeds
            urls = [
                "https://example.com/rss1",
                "https://example.com/rss2",
                "https://example.com/rss3",
            ]
            
            for url in urls:
                Feed.add_feed(session, url)
            
            # Verify all feeds are in database
            all_feeds = Feed.list_all(session)
            assert len(all_feeds) == 3
            
            all_urls = [feed.url for feed in all_feeds]
            for url in urls:
                assert url in all_urls
        finally:
            session.close()

