"""Integration tests for feed remove command."""
import pytest
import importlib
from pathlib import Path

# Import modules to enable reloading
import src.config
import src.services.storage as storage_module


@pytest.mark.integration
class TestFeedRemoveCommand:
    """Integration tests for feed remove CLI command."""
    
    def teardown_method(self):
        """Close database after each test."""
        from src.services.storage import close_database
        close_database()
        importlib.reload(src.config)
        importlib.reload(storage_module)
    
    def test_feed_remove_with_valid_id(self, clean_environment, monkeypatch, tmp_path):
        """Test feed remove command with valid feed ID."""
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
            # Add a feed first
            url = "https://example.com/rss"
            feed = Feed.add_feed(session, url)
            feed_id = feed.id
            
            # Verify feed exists
            assert Feed.get_by_id(session, feed_id) is not None
            
            # Remove the feed
            removed = Feed.remove_feed(session, feed_id)
            
            # Verify removal
            assert removed is True
            
            # Verify feed no longer exists
            assert Feed.get_by_id(session, feed_id) is None
        finally:
            session.close()
    
    def test_feed_remove_with_invalid_id(self, clean_environment, monkeypatch, tmp_path):
        """Test feed remove command with non-existent feed ID."""
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
            # Try to remove non-existent feed
            removed = Feed.remove_feed(session, 999)
            
            # Verify removal failed
            assert removed is False
        finally:
            session.close()
    
    def test_feed_remove_removes_only_target_feed(self, clean_environment, monkeypatch, tmp_path):
        """Test that removing one feed doesn't affect others."""
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
            
            # Verify all feeds exist
            all_feeds = Feed.list_all(session)
            assert len(all_feeds) == 3
            
            # Remove middle feed
            target_id = created_feeds[1].id
            removed = Feed.remove_feed(session, target_id)
            assert removed is True
            
            # Verify only target feed was removed
            remaining_feeds = Feed.list_all(session)
            assert len(remaining_feeds) == 2
            
            # Verify other feeds are intact
            remaining_ids = [feed.id for feed in remaining_feeds]
            assert created_feeds[0].id in remaining_ids
            assert created_feeds[2].id in remaining_ids
            assert target_id not in remaining_ids
        finally:
            session.close()
    
    def test_feed_remove_can_remove_first_feed(self, clean_environment, monkeypatch, tmp_path):
        """Test removing the first feed in the list."""
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
            
            # Remove first feed
            target_id = created_feeds[0].id
            removed = Feed.remove_feed(session, target_id)
            assert removed is True
            
            # Verify only one feed remains
            remaining_feeds = Feed.list_all(session)
            assert len(remaining_feeds) == 2
        finally:
            session.close()
    
    def test_feed_remove_can_remove_last_feed(self, clean_environment, monkeypatch, tmp_path):
        """Test removing the last feed in the list."""
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
            
            # Remove last feed
            target_id = created_feeds[2].id
            removed = Feed.remove_feed(session, target_id)
            assert removed is True
            
            # Verify only two feeds remain
            remaining_feeds = Feed.list_all(session)
            assert len(remaining_feeds) == 2
        finally:
            session.close()
    
    def test_feed_remove_with_multiple_calls(self, clean_environment, monkeypatch, tmp_path):
        """Test that removing the same feed twice fails on second call."""
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
            feed_id = feed.id
            
            # First removal should succeed
            removed1 = Feed.remove_feed(session, feed_id)
            assert removed1 is True
            
            # Second removal should fail
            removed2 = Feed.remove_feed(session, feed_id)
            assert removed2 is False
        finally:
            session.close()

