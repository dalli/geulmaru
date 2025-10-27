"""Unit tests for Feed model."""
import pytest
import importlib
from pathlib import Path

# Import modules to enable reloading
import src.config
import src.models.feed as feed_module
import src.services.storage as storage_module


@pytest.mark.unit
class TestFeedModel:
    """Tests for Feed model."""
    
    def teardown_method(self):
        """Close database after each test."""
        from src.services.storage import close_database
        close_database()
        importlib.reload(src.config)
        importlib.reload(storage_module)
        # Don't reload feed_module as it causes SQLAlchemy table conflicts
    
    def test_add_feed_validates_url_format(self, clean_environment, monkeypatch, tmp_path):
        """Test that add_feed validates URL format (T020)."""
        # Reload modules
        importlib.reload(src.config)
        importlib.reload(storage_module)
        
        # Set temporary database path
        test_db = str(tmp_path / "test.db")
        monkeypatch.setenv("GEULMARU_DB_PATH", test_db)
        
        from src.services.storage import init_database, create_tables, get_session
        from src.models.feed import Feed
        
        # Initialize database
        init_database()
        create_tables()
        
        session = get_session()
        try:
            # Test invalid URL without scheme
            with pytest.raises(ValueError, match="Invalid URL format"):
                Feed.add_feed(session, "invalid-url")
            
            # Test invalid URL without netloc
            with pytest.raises(ValueError, match="Invalid URL format"):
                Feed.add_feed(session, "http://")
            
            # Test invalid protocol (not http/https)
            with pytest.raises(ValueError, match="URL must use HTTP or HTTPS protocol"):
                Feed.add_feed(session, "ftp://example.com/rss")
        finally:
            session.close()
    
    def test_add_feed_creates_feed_successfully(self, clean_environment, monkeypatch, tmp_path):
        """Test that add_feed creates a feed successfully (T019)."""
        # Reload modules
        importlib.reload(src.config)
        importlib.reload(storage_module)
        
        # Set temporary database path
        test_db = str(tmp_path / "test.db")
        monkeypatch.setenv("GEULMARU_DB_PATH", test_db)
        
        from src.services.storage import init_database, create_tables, get_session
        from src.models.feed import Feed
        
        # Initialize database
        init_database()
        create_tables()
        
        session = get_session()
        try:
            # Add a valid feed
            url = "https://example.com/rss"
            feed = Feed.add_feed(session, url)
            
            # Verify feed was created
            assert feed is not None
            assert feed.id is not None
            assert feed.url == url
            assert feed.created_at is not None
            
            # Verify feed can be retrieved
            retrieved = session.query(Feed).filter(Feed.url == url).first()
            assert retrieved is not None
            assert retrieved.id == feed.id
        finally:
            session.close()
    
    def test_add_feed_detects_duplicates(self, clean_environment, monkeypatch, tmp_path):
        """Test that add_feed detects duplicate URLs (T020)."""
        # Reload modules
        importlib.reload(src.config)
        importlib.reload(storage_module)
        
        # Set temporary database path
        test_db = str(tmp_path / "test.db")
        monkeypatch.setenv("GEULMARU_DB_PATH", test_db)
        
        from src.services.storage import init_database, create_tables, get_session
        from src.models.feed import Feed
        
        # Initialize database
        init_database()
        create_tables()
        
        session = get_session()
        try:
            url = "https://example.com/rss"
            
            # Add first feed
            Feed.add_feed(session, url)
            
            # Try to add duplicate
            with pytest.raises(ValueError, match="Feed URL already exists"):
                Feed.add_feed(session, url)
        finally:
            session.close()
    
    def test_add_feed_validates_valid_urls(self, clean_environment, monkeypatch, tmp_path):
        """Test that add_feed accepts valid HTTP and HTTPS URLs (T020)."""
        # Reload modules
        importlib.reload(src.config)
        importlib.reload(storage_module)
        
        # Set temporary database path
        test_db = str(tmp_path / "test.db")
        monkeypatch.setenv("GEULMARU_DB_PATH", test_db)
        
        from src.services.storage import init_database, create_tables, get_session
        from src.models.feed import Feed
        
        # Initialize database
        init_database()
        create_tables()
        
        session = get_session()
        try:
            # Test HTTP URL
            http_feed = Feed.add_feed(session, "http://example.com/rss")
            assert http_feed.url == "http://example.com/rss"
            
            # Test HTTPS URL
            https_feed = Feed.add_feed(session, "https://example.com/rss2")
            assert https_feed.url == "https://example.com/rss2"
        finally:
            session.close()
    
    def test_list_all_feeds(self, clean_environment, monkeypatch, tmp_path):
        """Test that list_all returns all feeds (T019)."""
        # Reload modules
        importlib.reload(src.config)
        importlib.reload(storage_module)
        
        # Set temporary database path
        test_db = str(tmp_path / "test.db")
        monkeypatch.setenv("GEULMARU_DB_PATH", test_db)
        
        from src.services.storage import init_database, create_tables, get_session
        from src.models.feed import Feed
        
        # Initialize database
        init_database()
        create_tables()
        
        session = get_session()
        try:
            # Add multiple feeds
            url1 = "https://example.com/rss1"
            url2 = "https://example.com/rss2"
            url3 = "https://example.com/rss3"
            
            Feed.add_feed(session, url1)
            Feed.add_feed(session, url2)
            Feed.add_feed(session, url3)
            
            # List all feeds
            all_feeds = Feed.list_all(session)
            
            assert len(all_feeds) == 3
            all_urls = [feed.url for feed in all_feeds]
            assert url1 in all_urls
            assert url2 in all_urls
            assert url3 in all_urls
        finally:
            session.close()

