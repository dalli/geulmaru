"""Unit tests for Article model."""
import pytest
import importlib
from datetime import datetime
from pathlib import Path

# Import modules to enable reloading
import src.config
import src.services.storage as storage_module


@pytest.mark.unit
class TestArticleModel:
    """Tests for Article model."""
    
    def teardown_method(self):
        """Close database after each test."""
        from src.services.storage import close_database
        close_database()
        importlib.reload(src.config)
        importlib.reload(storage_module)
    
    def test_add_article_creates_article_successfully(self, clean_environment, monkeypatch, tmp_path):
        """Test that add_article creates an article successfully (T049)."""
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
            # Create a feed first
            feed_url = "https://example.com/rss"
            feed = Feed.add_feed(session, feed_url)
            
            # Add an article
            article_url = "https://example.com/article1"
            title = "Test Article"
            author = "Test Author"
            body = "This is the article body."
            
            article = Article.add_article(
                session,
                feed_id=feed.id,
                url=article_url,
                title=title,
                author=author,
                body=body
            )
            
            # Verify article was created
            assert article is not None
            assert article.id is not None
            assert article.feed_id == feed.id
            assert article.url == article_url
            assert article.title == title
            assert article.author == author
            assert article.body == body
            assert article.created_at is not None
            
            # Verify article can be retrieved
            retrieved = session.query(Article).filter(Article.url == article_url).first()
            assert retrieved is not None
            assert retrieved.id == article.id
        finally:
            session.close()
    
    def test_add_article_detects_duplicates(self, clean_environment, monkeypatch, tmp_path):
        """Test that add_article detects duplicate URLs (T049)."""
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
            # Create a feed first
            feed_url = "https://example.com/rss"
            feed = Feed.add_feed(session, feed_url)
            
            article_url = "https://example.com/article1"
            title = "Test Article"
            
            # Add first article
            Article.add_article(
                session,
                feed_id=feed.id,
                url=article_url,
                title=title
            )
            
            # Try to add duplicate
            with pytest.raises(ValueError, match="Article URL already exists"):
                Article.add_article(
                    session,
                    feed_id=feed.id,
                    url=article_url,
                    title="Different Title"
                )
        finally:
            session.close()
    
    def test_list_recent_with_no_articles(self, clean_environment, monkeypatch, tmp_path):
        """Test list_recent returns empty list when no articles exist (T049)."""
        # Reload modules
        importlib.reload(src.config)
        importlib.reload(storage_module)
        
        # Set temporary database path
        test_db = str(tmp_path / "test.db")
        monkeypatch.setenv("GEULMARU_DB_PATH", test_db)
        
        from src.services.storage import init_database, create_tables, get_session
        from src.models.article import Article
        
        # Initialize database
        init_database()
        create_tables()
        
        session = get_session()
        try:
            # List recent with no articles
            articles = Article.list_recent(session, limit=10)
            
            assert len(articles) == 0
        finally:
            session.close()
    
    def test_list_recent_with_multiple_articles(self, clean_environment, monkeypatch, tmp_path):
        """Test list_recent returns articles in correct order (T049)."""
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
            # Create a feed first
            feed = Feed.add_feed(session, "https://example.com/rss")
            
            # Add multiple articles
            for i in range(5):
                Article.add_article(
                    session,
                    feed_id=feed.id,
                    url=f"https://example.com/article{i}",
                    title=f"Article {i}"
                )
            
            # List recent articles
            articles = Article.list_recent(session, limit=10)
            
            # Verify all articles are returned
            assert len(articles) == 5
            
            # Verify articles are ordered by created_at descending
            for i in range(len(articles) - 1):
                assert articles[i].created_at >= articles[i+1].created_at
        finally:
            session.close()
    
    def test_list_recent_with_limit(self, clean_environment, monkeypatch, tmp_path):
        """Test list_recent respects limit parameter (T049)."""
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
            # Create a feed first
            feed = Feed.add_feed(session, "https://example.com/rss")
            
            # Add multiple articles
            for i in range(10):
                Article.add_article(
                    session,
                    feed_id=feed.id,
                    url=f"https://example.com/article{i}",
                    title=f"Article {i}"
                )
            
            # List with limit
            articles = Article.list_recent(session, limit=3)
            
            # Verify limit is respected
            assert len(articles) == 3
        finally:
            session.close()
    
    def test_get_by_url_finds_article(self, clean_environment, monkeypatch, tmp_path):
        """Test get_by_url finds article by URL (T049)."""
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
            # Create a feed first
            feed = Feed.add_feed(session, "https://example.com/rss")
            
            # Add an article
            article_url = "https://example.com/article1"
            article = Article.add_article(
                session,
                feed_id=feed.id,
                url=article_url,
                title="Test Article"
            )
            
            # Get by URL
            retrieved = Article.get_by_url(session, article_url)
            
            assert retrieved is not None
            assert retrieved.id == article.id
            assert retrieved.url == article_url
        finally:
            session.close()
    
    def test_get_by_url_returns_none_for_missing(self, clean_environment, monkeypatch, tmp_path):
        """Test get_by_url returns None for non-existent URL (T049)."""
        # Reload modules
        importlib.reload(src.config)
        importlib.reload(storage_module)
        
        # Set temporary database path
        test_db = str(tmp_path / "test.db")
        monkeypatch.setenv("GEULMARU_DB_PATH", test_db)
        
        from src.services.storage import init_database, create_tables, get_session
        from src.models.article import Article
        
        # Initialize database
        init_database()
        create_tables()
        
        session = get_session()
        try:
            # Get by non-existent URL
            retrieved = Article.get_by_url(session, "https://nonexistent.com/article")
            
            assert retrieved is None
        finally:
            session.close()
    
    def test_exists_by_url_checks_for_existence(self, clean_environment, monkeypatch, tmp_path):
        """Test exists_by_url checks for article existence (T049)."""
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
            # Create a feed first
            feed = Feed.add_feed(session, "https://example.com/rss")
            
            # Add an article
            article_url = "https://example.com/article1"
            Article.add_article(
                session,
                feed_id=feed.id,
                url=article_url,
                title="Test Article"
            )
            
            # Check existence
            assert Article.exists_by_url(session, article_url) is True
            assert Article.exists_by_url(session, "https://nonexistent.com/article") is False
        finally:
            session.close()
    
    def test_search_by_keyword_finds_matching_articles(self, clean_environment, monkeypatch, tmp_path):
        """Test search_by_keyword finds articles containing keyword (T049)."""
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
            # Create a feed first
            feed = Feed.add_feed(session, "https://example.com/rss")
            
            # Add articles with different titles
            Article.add_article(
                session,
                feed_id=feed.id,
                url="https://example.com/article1",
                title="Python Programming",
                body="This is about Python"
            )
            Article.add_article(
                session,
                feed_id=feed.id,
                url="https://example.com/article2",
                title="Java Programming",
                body="This is about Java"
            )
            Article.add_article(
                session,
                feed_id=feed.id,
                url="https://example.com/article3",
                title="Python Tips",
                body="More Python content"
            )
            
            # Search for Python
            results = Article.search_by_keyword(session, "Python")
            
            # Verify results
            assert len(results) == 2
            assert all("Python" in article.title or "Python" in article.body for article in results)
        finally:
            session.close()

