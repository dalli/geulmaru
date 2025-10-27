"""Unit tests for database storage service."""
import os
import pytest
import importlib
from pathlib import Path

# Import modules to enable reloading
import src.config
import src.services.storage as storage_module


@pytest.mark.unit
class TestDatabaseInitialization:
    """Tests for database initialization."""
    
    def teardown_method(self):
        """Close database after each test."""
        # Close database and reload modules to get fresh state
        from src.services.storage import close_database
        close_database()
        importlib.reload(src.config)
        importlib.reload(storage_module)
    
    def test_init_database_creates_engine(self, clean_environment, monkeypatch, tmp_path):
        """Test that init_database creates a database engine."""
        # Reload modules to get clean state
        importlib.reload(src.config)
        importlib.reload(storage_module)
        
        # Set temporary database path
        test_db = str(tmp_path / "test.db")
        monkeypatch.setenv("GEULMARU_DB_PATH", test_db)
        
        from src.services.storage import init_database, create_tables
        
        init_database()
        create_tables()
        
        # Verify database file was created
        assert Path(test_db).exists()
    
    def test_create_tables_creates_tables(self, clean_environment, monkeypatch, tmp_path):
        """Test that create_tables creates database tables."""
        # Reload modules
        importlib.reload(src.config)
        importlib.reload(storage_module)
        
        # Set temporary database path
        test_db = str(tmp_path / "test.db")
        monkeypatch.setenv("GEULMARU_DB_PATH", test_db)
        
        from src.services.storage import init_database, create_tables, get_session
        
        init_database()
        create_tables()
        
        # Verify database file exists
        assert Path(test_db).exists()
        
        # Verify we can get a session (implies tables exist)
        session = get_session()
        assert session is not None
        session.close()
    
    def test_database_exists_check(self, clean_environment, monkeypatch, tmp_path):
        """Test checking if database exists."""
        # Reload modules
        importlib.reload(src.config)
        importlib.reload(storage_module)
        
        # Set temporary database path
        test_db = str(tmp_path / "test.db")
        monkeypatch.setenv("GEULMARU_DB_PATH", test_db)
        
        from src.services.storage import check_database_exists, init_database, create_tables
        
        # Database should not exist initially
        assert not check_database_exists()
        
        # Create database
        init_database()
        create_tables()
        
        # Database should now exist
        assert check_database_exists()
    
    def test_reset_database_drops_tables(self, clean_environment, monkeypatch, tmp_path):
        """Test that reset_database drops and recreates tables."""
        # Reload modules
        importlib.reload(src.config)
        importlib.reload(storage_module)
        
        # Set temporary database path
        test_db = str(tmp_path / "test.db")
        monkeypatch.setenv("GEULMARU_DB_PATH", test_db)
        
        from src.services.storage import init_database, create_tables, reset_database
        
        # Create initial database
        init_database()
        create_tables()
        
        # Verify database exists
        assert Path(test_db).exists()
        
        # Reset database
        reset_database()
        
        # Database should still exist but tables should be fresh
        assert Path(test_db).exists()
    
    def test_create_tables_without_init_raises_error(self, clean_environment, monkeypatch, tmp_path):
        """Test that create_tables raises error if database not initialized."""
        # Reload modules
        importlib.reload(src.config)
        importlib.reload(storage_module)
        
        from src.services.storage import create_tables
        
        # Should raise RuntimeError
        with pytest.raises(RuntimeError, match="Database not initialized"):
            create_tables()
    
    def test_get_session_without_init_raises_error(self, clean_environment, monkeypatch):
        """Test that get_session raises error if database not initialized."""
        # Reload modules
        importlib.reload(src.config)
        importlib.reload(storage_module)
        
        from src.services.storage import get_session
        
        # Should raise RuntimeError
        with pytest.raises(RuntimeError, match="Database not initialized"):
            get_session()
