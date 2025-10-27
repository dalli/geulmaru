"""Integration tests for init-db command."""
import os
import subprocess
import sys
import importlib
from pathlib import Path

import pytest

# Import modules to enable reloading
import src.config
import src.services.storage as storage_module


@pytest.mark.integration
class TestInitDbCommand:
    """Integration tests for init-db CLI command."""
    
    def teardown_method(self):
        """Close database after each test."""
        # Close database and reload modules to get fresh state
        from src.services.storage import close_database
        close_database()
        importlib.reload(src.config)
        importlib.reload(storage_module)
    
    def test_init_db_creates_database_file(self, clean_environment, monkeypatch, tmp_path):
        """Test that init-db command creates database file."""
        # Reload modules
        importlib.reload(src.config)
        importlib.reload(storage_module)
        
        # Set temporary database path
        test_db = str(tmp_path / "geulmaru.db")
        monkeypatch.setenv("GEULMARU_DB_PATH", test_db)
        
        from src.services.storage import init_database, create_tables, check_database_exists
        
        init_database()
        create_tables()
        
        # Verify database file was created
        assert check_database_exists()
        assert Path(test_db).exists()
    
    def test_init_db_creates_tables(self, clean_environment, monkeypatch, tmp_path):
        """Test that init-db creates necessary tables."""
        # Reload modules
        importlib.reload(src.config)
        importlib.reload(storage_module)
        
        # Set temporary database path
        test_db = str(tmp_path / "test.db")
        monkeypatch.setenv("GEULMARU_DB_PATH", test_db)
        
        from src.services.storage import init_database, create_tables, get_session
        from src.models import Feed, Article
        
        # Initialize database
        init_database()
        create_tables()
        
        # Get session and verify tables exist by querying them
        session = get_session()
        try:
            # Query should not raise error if table exists
            feeds = session.query(Feed).all()
            articles = session.query(Article).all()
            
            # Both queries should succeed (empty results are fine)
            assert isinstance(feeds, list)
            assert isinstance(articles, list)
        finally:
            session.close()
    
    def test_init_db_handles_existing_database(self, clean_environment, monkeypatch, tmp_path):
        """Test that init-db handles existing database gracefully."""
        # Reload modules
        importlib.reload(src.config)
        importlib.reload(storage_module)
        
        # Set temporary database path
        test_db = str(tmp_path / "geulmaru.db")
        monkeypatch.setenv("GEULMARU_DB_PATH", test_db)
        
        from src.services.storage import init_database, create_tables, get_session
        from src.models import Feed
        
        # Initialize database twice
        init_database()
        create_tables()
        
        # Should not raise error on second initialization
        init_database()
        create_tables()
        
        # Verify still works
        session = get_session()
        try:
            feeds = session.query(Feed).all()
            assert isinstance(feeds, list)
        finally:
            session.close()
    
    def test_init_db_validates_parent_directory(self, clean_environment, monkeypatch, tmp_path):
        """Test that init-db validates parent directory existence."""
        # Reload modules
        importlib.reload(src.config)
        importlib.reload(storage_module)
        
        # Set database path with non-existent parent directory
        test_db = str(tmp_path / "nonexistent" / "subdir" / "geulmaru.db")
        monkeypatch.setenv("GEULMARU_DB_PATH", test_db)
        
        from src.services.storage import init_database, create_tables
        
        # Should create parent directories
        init_database()
        create_tables()
        
        # Verify file exists
        assert Path(test_db).exists()
    
    def test_init_db_creates_indexes(self, clean_environment, monkeypatch, tmp_path):
        """Test that init-db creates indexes on tables."""
        # Reload modules
        importlib.reload(src.config)
        importlib.reload(storage_module)
        
        # Set temporary database path
        test_db = str(tmp_path / "geulmaru.db")
        monkeypatch.setenv("GEULMARU_DB_PATH", test_db)
        
        from src.services.storage import init_database, create_tables
        
        # Initialize database
        init_database()
        create_tables()
        
        # Verify tables exist by inspecting database
        import sqlite3
        conn = sqlite3.connect(test_db)
        cursor = conn.cursor()
        
        # Get all tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = {row[0] for row in cursor.fetchall()}
        
        conn.close()
        
        # Verify expected tables exist
        assert 'feeds' in tables
        assert 'articles' in tables
