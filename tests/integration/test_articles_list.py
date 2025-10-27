"""Integration tests for articles list command."""
import pytest
import importlib
from pathlib import Path

# Import modules to enable reloading
import src.config
import src.services.storage as storage_module


@pytest.mark.integration
class TestArticlesListCommand:
    """Integration tests for articles list CLI command."""
    
    def teardown_method(self):
        """Close database after each test."""
        from src.services.storage import close_database
        close_database()
        importlib.reload(src.config)
        importlib.reload(storage_module)
    
    def test_articles_list_when_empty(self, clean_environment, monkeypatch, tmp_path):
        """Test articles list command when no articles are registered (T050)."""
        # Reload modules
        importlib.reload(src.config)
        importlib.reload(storage_module)
        
        # Set temporary database path
        test_db = str(tmp_path / "test.db")
        monkeypatch.setenv("GEULMARU_DB_PATH", test_db)
        
        from src.services.storage import init_database, create_tables
        from src.models.article import Article
        from src.services.storage import get_session
        
        # Initialize database
        init_database()
        create_tables()
        
        session = get_session()
        try:
            # Verify empty list
            articles = Article.list_recent(session, limit=10)
            assert len(articles) == 0
        finally:
            session.close()
    
    def test_articles_list_with_multiple_articles(self, clean_environment, monkeypatch, tmp_path):
        """Test articles list command with multiple articles (T050)."""
        # Reload modules
        importlib.reload(src.config)
        importlib.reload(storage_module)
        
        # Set temporary database path
        test_db = str(tmp_path / "test.db")
        monkeypatch.setenv("GEULMARU_DB_PATH", test_db)
        
        from src.services.storage import init_database, create_tables, get_session
        from src.models.article import Article
        from src.models.feed import Feed
        
        # Initialize database
        init_database()
        create_tables()
        
        session = get_session()
        try:
            # Create a feed
            feed = Feed.add_feed(session, "https://example.com/rss")
            
            # Add multiple articles
            for i in range(5):
                Article.add_article(
                    session,
                    feed_id=feed.id,
                    url=f"https://example.com/article{i}",
                    title=f"Test Article {i}",
                    author=f"Author {i}",
                    body=f"Body content for article {i}"
                )
            
            # List recent articles
            articles = Article.list_recent(session, limit=10)
            
            # Verify all articles are returned
            assert len(articles) == 5
            
            # Verify articles are ordered by created_at descending (most recent first)
            for i in range(len(articles) - 1):
                assert articles[i].created_at >= articles[i+1].created_at
            
            # Verify each article has required attributes
            for article in articles:
                assert article.id is not None
                assert article.feed_id == feed.id
                assert article.url is not None
                assert article.title is not None
                assert article.created_at is not None
        finally:
            session.close()
    
    def test_articles_list_with_limit(self, clean_environment, monkeypatch, tmp_path):
        """Test articles list command respects limit parameter (T050)."""
        # Reload modules
        importlib.reload(src.config)
        importlib.reload(storage_module)
        
        # Set temporary database path
        test_db = str(tmp_path / "test.db")
        monkeypatch.setenv("GEULMARU_DB_PATH", test_db)
        
        from src.services.storage import init_database, create_tables, get_session
        from src.models.article import Article
        from src.models.feed import Feed
        
        # Initialize database
        init_database()
        create_tables()
        
        session = get_session()
        try:
            # Create a feed
            feed = Feed.add_feed(session, "https://example.com/rss")
            
            # Add multiple articles
            for i in range(10):
                Article.add_article(
                    session,
                    feed_id=feed.id,
                    url=f"https://example.com/article{i}",
                    title=f"Test Article {i}"
                )
            
            # List with limit
            articles = Article.list_recent(session, limit=3)
            
            # Verify limit is respected
            assert len(articles) == 3
            
            # Verify most recent articles are returned
            all_articles = Article.list_recent(session, limit=10)
            assert articles[0].id == all_articles[0].id
            assert articles[1].id == all_articles[1].id
            assert articles[2].id == all_articles[2].id
        finally:
            session.close()
    
    def test_articles_list_with_single_article(self, clean_environment, monkeypatch, tmp_path):
        """Test articles list command with a single article (T050)."""
        # Reload modules
        importlib.reload(src.config)
        importlib.reload(storage_module)
        
        # Set temporary database path
        test_db = str(tmp_path / "test.db")
        monkeypatch.setenv("GEULMARU_DB_PATH", test_db)
        
        from src.services.storage import init_database, create_tables, get_session
        from src.models.article import Article
        from src.models.feed import Feed
        
        # Initialize database
        init_database()
        create_tables()
        
        session = get_session()
        try:
            # Create a feed
            feed = Feed.add_feed(session, "https://example.com/rss")
            
            # Add a single article
            article = Article.add_article(
                session,
                feed_id=feed.id,
                url="https://example.com/article1",
                title="Test Article",
                author="Test Author",
                body="Test body"
            )
            
            # List articles
            articles = Article.list_recent(session, limit=10)
            
            # Verify single article is returned
            assert len(articles) == 1
            assert articles[0].id == article.id
            assert articles[0].url == article.url
            assert articles[0].title == article.title
            assert articles[0].author == article.author
            assert articles[0].body == article.body
        finally:
            session.close()
    
    def test_articles_list_preserves_data_integrity(self, clean_environment, monkeypatch, tmp_path):
        """Test that list command preserves article data integrity (T050)."""
        # Reload modules
        importlib.reload(src.config)
        importlib.reload(storage_module)
        
        # Set temporary database path
        test_db = str(tmp_path / "test.db")
        monkeypatch.setenv("GEULMARU_DB_PATH", test_db)
        
        from src.services.storage import init_database, create_tables, get_session
        from src.models.article import Article
        from src.models.feed import Feed
        
        # Initialize database
        init_database()
        create_tables()
        
        session = get_session()
        try:
            # Create a feed
            feed = Feed.add_feed(session, "https://example.com/rss")
            
            # Add an article
            article = Article.add_article(
                session,
                feed_id=feed.id,
                url="https://example.com/article1",
                title="Test Article",
                author="Test Author",
                body="Test body"
            )
            
            # List articles multiple times (read operations)
            for _ in range(5):
                articles = Article.list_recent(session, limit=10)
                assert len(articles) == 1
                assert articles[0].url == article.url
                assert articles[0].title == article.title
            
            # Verify data is intact
            retrieved = Article.get_by_url(session, article.url)
            assert retrieved is not None
            assert retrieved.url == article.url
            assert retrieved.title == article.title
            assert retrieved.id == article.id
        finally:
            session.close()
    
    def test_articles_list_with_different_feeds(self, clean_environment, monkeypatch, tmp_path):
        """Test articles list from different feeds (T050)."""
        # Reload modules
        importlib.reload(src.config)
        importlib.reload(storage_module)
        
        # Set temporary database path
        test_db = str(tmp_path / "test.db")
        monkeypatch.setenv("GEULMARU_DB_PATH", test_db)
        
        from src.services.storage import init_database, create_tables, get_session
        from src.models.article import Article
        from src.models.feed import Feed
        
        # Initialize database
        init_database()
        create_tables()
        
        session = get_session()
        try:
            # Create multiple feeds
            feed1 = Feed.add_feed(session, "https://example.com/rss1")
            feed2 = Feed.add_feed(session, "https://example.com/rss2")
            
            # Add articles to different feeds
            for i in range(3):
                Article.add_article(
                    session,
                    feed_id=feed1.id,
                    url=f"https://example.com/feed1-article{i}",
                    title=f"Feed1 Article {i}"
                )
                Article.add_article(
                    session,
                    feed_id=feed2.id,
                    url=f"https://example.com/feed2-article{i}",
                    title=f"Feed2 Article {i}"
                )
            
            # List all articles
            articles = Article.list_recent(session, limit=10)
            
            # Verify all articles from both feeds are returned
            assert len(articles) == 6
            
            # Group by feed
            feed1_articles = [a for a in articles if a.feed_id == feed1.id]
            feed2_articles = [a for a in articles if a.feed_id == feed2.id]
            
            assert len(feed1_articles) == 3
            assert len(feed2_articles) == 3
        finally:
            session.close()

