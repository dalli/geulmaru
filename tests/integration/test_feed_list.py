"""Integration tests for feed list command."""
import pytest
import importlib
from pathlib import Path

# Import modules to enable reloading
import src.config
import src.services.storage as storage_module


@pytest.mark.integration
class TestFeedListCommand:
    """Integration tests for feed list CLI command."""
    
    def teardown_method(self):
        """Close database after each test."""
        from src.services.storage import close_database
        close_database()
        importlib.reload(src.config)
        importlib.reload(storage_module)
    
    def test_feed_list_when_empty(self, clean_environment, monkeypatch, tmp_path):
        """Test feed list command when no feeds are registered."""
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
            # Verify empty list
            feeds = Feed.list_all(session)
            assert len(feeds) == 0
        finally:
            session.close()
    
    def test_feed_list_with_multiple_feeds(self, clean_environment, monkeypatch, tmp_path):
        """Test feed list command with multiple registered feeds."""
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
            
            created_feeds = []
            for url in urls:
                feed = Feed.add_feed(session, url)
                created_feeds.append(feed)
            
            # List all feeds
            feeds = Feed.list_all(session)
            
            # Verify all feeds are returned
            assert len(feeds) == 3
            
            # Verify feeds are ordered by created_at descending
            assert feeds[0].created_at >= feeds[1].created_at
            assert feeds[1].created_at >= feeds[2].created_at
            
            # Verify all URLs are present
            feed_urls = [feed.url for feed in feeds]
            for url in urls:
                assert url in feed_urls
            
            # Verify each feed has required attributes
            for feed in feeds:
                assert feed.id is not None
                assert feed.url is not None
                assert feed.created_at is not None
                
        finally:
            session.close()
    
    def test_feed_list_with_single_feed(self, clean_environment, monkeypatch, tmp_path):
        """Test feed list command with a single registered feed."""
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
            # Add a single feed
            url = "https://example.com/rss"
            created_feed = Feed.add_feed(session, url)
            
            # List all feeds
            feeds = Feed.list_all(session)
            
            # Verify single feed is returned
            assert len(feeds) == 1
            assert feeds[0].id == created_feed.id
            assert feeds[0].url == url
            assert feeds[0].created_at == created_feed.created_at
            
        finally:
            session.close()
    
    def test_feed_list_preserves_feed_data(self, clean_environment, monkeypatch, tmp_path):
        """Test that damaged list command preserves feed data integrity."""
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
            # Add a feed
            url = "https://example.com/rss"
            feed = Feed.add_feed(session, url)
            
            # List feeds multiple times (read operations)
            for _ in range(5):
                feeds = Feed.list_all(session)
                assert len(feeds) == 1
                assert feeds[0].url == url
            
            # Verify data is intact
            retrieved = Feed.get_by_id(session, feed.id)
            assert retrieved is not None
            assert retrieved.url == url
            assert retrieved.id == feed.id
            
        finally:
            session.close()

