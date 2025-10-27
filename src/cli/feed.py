"""CLI commands for feed management."""
import logging
import typer

from src.models.feed import Feed
from src.services.storage import get_session, init_database, create_tables
from src.config import setup_logging

# Setup logger
logger = logging.getLogger(__name__)


def add_feed_command(url: str):
    """Add a new RSS feed to the database.
    
    Args:
        url: RSS feed URL to add
    """
    # Setup logging
    setup_logging()
    
    try:
        # Ensure database is initialized
        from src.services.storage import _engine
        if _engine is None:
            logger.info("Database not initialized, initializing...")
            init_database()
            create_tables()
        
        # Get database session
        session = get_session()
        
        try:
            # Add feed
            feed = Feed.add_feed(session, url)
            
            # Log success
            logger.info(f"Successfully added feed: {url} (ID: {feed.id})")
            
            # Display success message
            typer.echo(f"✅ Feed added successfully!")
            typer.echo(f"   ID: {feed.id}")
            typer.echo(f"   URL: {feed.url}")
            typer.echo(f"   Created: {feed.created_at}")
            
        except ValueError as e:
            # Log error
            logger.error(f"Failed to add feed: {e}")
            
            # Display error message
            typer.echo(f"❌ Error: {e}", err=True)
            raise typer.Exit(1)
        
        finally:
            session.close()
    
    except Exception as e:
        logger.error(f"Unexpected error adding feed: {e}")
        typer.echo(f"❌ Unexpected error: {e}", err=True)
        raise typer.Exit(1)


def list_feeds_command():
    """List all registered RSS feeds."""
    # Setup logging
    setup_logging()
    
    try:
        # Ensure database is initialized
        from src.services.storage import _engine
        if _engine is None:
            logger.info("Database not initialized, initializing...")
            init_database()
            create_tables()
        
        # Get database session
        session = get_session()
        
        try:
            # Get all feeds
            feeds = Feed.list_all(session)
            
            # Log operation
            logger.info(f"Listing {len(feeds)} feeds")
            
            # Display results
            if not feeds:
                typer.echo("📋 No feeds registered yet.")
                typer.echo("   Use 'geulmaru feed add <URL>' to add a feed.")
                return
            
            typer.echo(f"📋 Registered RSS feeds ({len(feeds)}):")
            typer.echo()
            
            for feed in feeds:
                typer.echo(f"   [{feed.id}] {feed.url}")
                typer.echo(f"       Created: {feed.created_at}")
                typer.echo()
        
        finally:
            session.close()
    
    except Exception as e:
        logger.error(f"Error listing feeds: {e}")
        typer.echo(f"❌ Error listing feeds: {e}", err=True)
        raise typer.Exit(1)


def remove_feed_command(feed_id: int):
    """Remove a RSS feed from the database.
    
    Args:
        feed_id: ID of the feed to remove
    """
    # Setup logging
    setup_logging()
    
    try:
        # Ensure database is initialized
        from src.services.storage import _engine
        if _engine is None:
            logger.info("Database not initialized, initializing...")
            init_database()
            create_tables()
        
        # Get database session
        session = get_session()
        
        try:
            # Remove feed
            removed = Feed.remove_feed(session, feed_id)
            
            if removed:
                # Log success
                logger.info(f"Successfully removed feed: ID {feed_id}")
                
                # Display success message
                typer.echo(f"✅ Feed {feed_id} removed successfully!")
            else:
                # Log not found
                logger.warning(f"Feed not found: ID {feed_id}")
                
                # Display error message
                typer.echo(f"❌ Feed with ID {feed_id} not found.", err=True)
                raise typer.Exit(1)
        
        finally:
            session.close()
    
    except typer.Exit:
        raise
    except Exception as e:
        logger.error(f"Error removing feed: {e}")
        typer.echo(f"❌ Error removing feed: {e}", err=True)
        raise typer.Exit(1)

