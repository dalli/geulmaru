"""CLI commands for article management."""
import logging
import typer

from src.models.article import Article
from src.models.feed import Feed
from src.services.storage import get_session, init_database, create_tables
from src.config import setup_logging

# Setup logger
logger = logging.getLogger(__name__)


def list_articles_command(limit: int = 10):
    """List recent articles from the archive.
    
    Args:
        limit: Maximum number of articles to display
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
            # Get recent articles
            articles = Article.list_recent(session, limit=limit)
            
            # Log operation
            logger.info(f"Listing {len(articles)} articles")
            
            # Display results
            if not articles:
                typer.echo("📰 No articles collected yet.")
                typer.echo("   Use 'geulmaru fetch-all' to collect articles from RSS feeds.")
                return
            
            typer.echo(f"📰 Recent articles (showing {len(articles)}):")
            typer.echo()
            
            for article in articles:
                # Get feed URL for display
                feed = Feed.get_by_id(session, article.feed_id)
                feed_url = feed.url if feed else "Unknown"
                
                # Format date
                created_str = article.created_at.strftime("%Y-%m-%d %H:%M:%S") if article.created_at else "N/A"
                
                # Display article
                typer.echo(f"   [{article.id}] {article.title}")
                
                if article.author:
                    typer.echo(f"       Author: {article.author}")
                
                typer.echo(f"       Feed: {feed_url}")
                typer.echo(f"       URL: {article.url}")
                typer.echo(f"       Collected: {created_str}")
                typer.echo()
        
        finally:
            session.close()
    
    except Exception as e:
        logger.error(f"Error listing articles: {e}")
        typer.echo(f"❌ Error listing articles: {e}", err=True)
        raise typer.Exit(1)

