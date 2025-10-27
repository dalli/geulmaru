"""Integration tests for articles search command."""
import pytest
import importlib
from pathlib import Path

# Import modules to enable reloading
import src.config
import src.services.storage as storage_module


@pytest.mark.integration
class TestArticlesSearchCommand:
    """Integration tests for articles search CLI command."""
    
    def teardown_method(self):
        """Close database after each test."""
        from src.services.storage import close_database
        close_database()
        importlib.reload(src.config)
        importlib.reload(storage_module)
    
    def test_search_by_keyword_finds_matching_articles_in_title(self, clean_environment, monkeypatch, tmp_path):
        """Test search finds articles with keyword in title (T059)."""
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
            
            # Add articles with different titles
            Article.add_article(
                session,
                feed_id=feed.id,
                url="https://example.com/article1",
                title="Python Programming Guide",
                body="Content about Python"
            )
            Article.add_article(
                session,
                feed_id=feed.id,
                url="https://example.com/article2",
                title="Java Programming Guide",
                body="Content about Java"
            )
            Article.add_article(
                session,
                feed_id=feed.id,
                url="https://example.com/article3",
                title="Python Tips and Tricks",
                body="More content"
            )
            
            # Search for Python
            results = Article.search_by_keyword(session, "Python", limit=50)
            
            # Verify results
            assert len(results) == 2
            assert all("Python" in article.title for article in results)
        finally:
            session.close()
    
    def test_search_by_keyword_finds_matching_articles_in_body(self, clean_environment, monkeypatch, tmp_path):
        """Test search finds articles with keyword in body (T059)."""
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
            
            # Add articles with keywords in body
            Article.add_article(
                session,
                feed_id=feed.id,
                url="https://example.com/article1",
                title="Article 1",
                body="This article discusses Python programming"
            )
            Article.add_article(
                session,
                feed_id=feed.id,
                url="https://example.com/article2",
                title="Article 2",
                body="This article discusses Java programming"
            )
            Article.add_article(
                session,
                feed_id=feed.id,
                url="https://example.com/article3",
                title="Article 3",
                body="More about Python and its features"
            )
            
            # Search for Python
            results = Article.search_by_keyword(session, "Python", limit=50)
            
            # Verify results
            assert len(results) == 2
            assert all("Python" in article.body for article in results)
        finally:
            session.close()
    
    def test_search_by_keyword_finds_matching_articles_in_title_or_body(self, clean_environment, monkeypatch, tmp_path):
        """Test search finds articles with keyword in title or body (T059)."""
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
            
            # Add articles with keyword in different places
            Article.add_article(
                session,
                feed_id=feed.id,
                url="https://example.com/article1",
                title="Python Programming",
                body="Content"
            )
            Article.add_article(
                session,
                feed_id=feed.id,
                url="https://example.com/article2",
                title="Article Title",
                body="About Python features"
            )
            Article.add_article(
                session,
                feed_id=feed.id,
                url="https://example.com/article3",
                title="Java Programming",
                body="Content"
            )
            
            # Search for Python
            results = Article.search_by_keyword(session, "Python", limit=50)
            
            # Verify results
            assert len(results) == 2
            assert all("Python" in article.title or "Python" in article.body for article in results)
        finally:
            session.close()
    
    def test_search_by_keyword_returns_empty_when_no_match(self, clean_environment, monkeypatch, tmp_path):
        """Test search returns empty list when no articles match (T059)."""
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
            
            # Add articles
            Article.add_article(
                session,
                feed_id=feed.id,
                url="https://example.com/article1",
                title="Java Programming",
                body="Content about Java"
            )
            
            # Search for non-existent keyword
            results = Article.search_by_keyword(session, "Python", limit=50)
            
            # Verify empty results
            assert len(results) == 0
        finally:
            session.close()
    
    def test_search_by_keyword_returns_empty_with_no_articles(self, clean_environment, monkeypatch, tmp_path):
        """Test search returns empty list when no articles exist (T059)."""
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
            # Search with no articles
            results = Article.search_by_keyword(session, "Python", limit=50)
            
            # Verify empty results
            assert len(results) == 0
        finally:
            session.close()
    
    def test_search_by_keyword_respects_limit(self, clean_environment, monkeypatch, tmp_path):
        """Test search respects limit parameter (T059)."""
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
            
            # Add multiple articles with keyword
            for i in range(10):
                Article.add_article(
                    session,
                    feed_id=feed.id,
                    url=f"https://example.com/article{i}",
                    title=f"Python Article {i}",
                    body=f"Content {i}"
                )
            
            # Search with limit
            results = Article.search_by_keyword(session, "Python", limit=3)
            
            # Verify limit is respected
            assert len(results) == 3
        finally:
            session.close()
    
    def test_search_by_keyword_returns_ordered_by_created_at_desc(self, clean_environment, monkeypatch, tmp_path):
        """Test search returns results ordered by created_at descending (T059)."""
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
                    title=f"Python Article {i}",
                    body=f"Content {i}"
                )
            
            # Search
            results = Article.search_by_keyword(session, "Python", limit=10)
            
            # Verify results are ordered by created_at descending
            for i in range(len(results) - 1):
                assert results[i].created_at >= results[i+1].created_at
        finally:
            session.close()
    
    def test_search_by_keyword_is_case_insensitive(self, clean_environment, monkeypatch, tmp_path):
        """Test search is case insensitive (T059)."""
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
            
            # Add articles with different cases
            Article.add_article(
                session,
                feed_id=feed.id,
                url="https://example.com/article1",
                title="Python Programming",
                body="Content"
            )
            Article.add_article(
                session,
                feed_id=feed.id,
                url="https://example.com/article2",
                title="python programming",
                body="Content"
            )
            
            # Search with uppercase
            results_upper = Article.search_by_keyword(session, "Python", limit=50)
            
            # Search with lowercase
            results_lower = Article.search_by_keyword(session, "python", limit=50)
            
            # Verify case insensitivity - both searches should find both articles
            assert len(results_upper) == 2
            assert len(results_lower) == 2
            assert all("python" in article.title.lower() or "Python" in article.title for article in results_upper)
        finally:
            session.close()

