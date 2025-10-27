"""CLI command for initializing the database."""
import typer

from src.services.storage import init_database, create_tables
from src.config import setup_logging


def init_db_command():
    """Initialize the database with necessary tables."""
    # Setup logging
    setup_logging()
    
    try:
        # Initialize database connection
        init_database()
        
        # Create tables
        create_tables()
        
        # Success message
        typer.echo("✅ Database initialized successfully!")
        
    except Exception as e:
        typer.echo(f"❌ Error initializing database: {e}", err=True)
        raise typer.Exit(1)
