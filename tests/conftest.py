"""
Pytest configuration and fixtures for RSS Collector tests.

This module provides shared fixtures and configuration for all tests.
"""
import pytest
import os
import sys
from pathlib import Path

# Add src to Python path for imports
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "src"))


@pytest.fixture(scope="session")
def test_db_path(tmp_path_factory):
    """Create a temporary database path for testing."""
    db_path = tmp_path_factory.mktemp("data") / "test_geulmaru.db"
    return str(db_path)


@pytest.fixture(scope="function")
def clean_environment(monkeypatch):
    """Ensure tests run with clean environment variables."""
    # Set test environment variables
    monkeypatch.setenv("GEULMARU_LOG_LEVEL", "DEBUG")
    monkeypatch.delenv("GEULMARU_DB_PATH", raising=False)


@pytest.fixture(scope="function")
def fixtures_dir():
    """Return path to test fixtures directory."""
    return Path(__file__).parent / "fixtures"

