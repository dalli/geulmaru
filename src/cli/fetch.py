"""CLI command for fetching articles from RSS feeds."""
import logging
import typer

from src.services.storage import get_db_session
from src.models.feed import Feed
from src.models.article import Article
from src.config import setup_logging

logger = logging.getLogger(__name__)

# Import shutdown checker
from src.shutdown import is_shutdown_requested


def fetch_all_command() -> None:
    """Fetch articles from all registered RSS feeds.
    
    This command will:
    1. Load all registered feeds
    2. Fetch RSS XML from each feed
    3. Parse RSS to extract article metadata
    4. Check for duplicates before scraping
    5. Scrape article content from URLs
    6. Store articles in database
    """
    # Setup logging
    setup_logging()
    
    logger.info("Starting fetch-all operation")
    
    stats = {
        'feeds_processed': 0,
        'articles_found': 0,
        'articles_scraped': 0,
        'articles_duplicates': 0,
        'articles_errors': 0,
    }
    
    try:
        with get_db_session() as db:
            feeds = Feed.list_all(db)
            
            if not feeds:
                typer.echo("No RSS feeds registered. Use 'feed add <URL>' to add feeds.")
                return
            
            logger.info(f"Found {len(feeds)} registered feeds")
            typer.echo(f"Processing {len(feeds)} RSS feed(s)...")
            
            for feed in feeds:
                # Check for shutdown request
                if is_shutdown_requested():
                    logger.info("Shutdown requested, stopping fetch operation")
                    typer.echo("\n⚠️  Shutdown requested. Stopping fetch operation...")
                    break
                
                stats['feeds_processed'] += 1
                typer.echo(f"\nFetching from: {feed.url}")
                
                try:
                    # Import here to enable testing with mock
                    from src.services.feed_fetcher import fetch_rss
                    
                    # Fetch RSS XML
                    rss_content = fetch_rss(feed.url)
                    
                    if not rss_content:
                        logger.warning(f"Failed to fetch RSS from: {feed.url}")
                        typer.echo("  → Failed to fetch RSS feed")
                        continue
                    
                    # Import here to enable testing with mock
                    from src.services.feed_parser import parse_rss
                    
                    # Parse RSS to get article metadata
                    articles_metadata = parse_rss(rss_content)
                    
                    if not articles_metadata:
                        logger.warning(f"No articles found in RSS feed: {feed.url}")
                        typer.echo("  → No articles found")
                        continue
                    
                    logger.info(f"Found {len(articles_metadata)} articles in feed")
                    stats['articles_found'] += len(articles_metadata)
                    
                    # Process each article
                    for article_meta in articles_metadata:
                        # Check for shutdown request
                        if is_shutdown_requested():
                            logger.info("Shutdown requested, stopping article processing")
                            typer.echo("\n⚠️  Shutdown requested. Stopping article processing...")
                            break
                        
                        article_url = article_meta['url']
                        
                        # Check for duplicates before scraping
                        if Article.exists_by_url(db, article_url):
                            logger.debug(f"Skipping duplicate: {article_url}")
                            stats['articles_duplicates'] += 1
                            continue
                        
                        # Import here to enable testing with mock
                        from src.services.article_scraper import scrape_article
                        
                        # Scrape article content
                        typer.echo(f"  → Scraping: {article_meta['title'][:50]}...")
                        
                        scraped_data = scrape_article(article_url)
                        
                        if not scraped_data:
                            logger.warning(f"Failed to scrape article: {article_url}")
                            stats['articles_errors'] += 1
                            continue
                        
                        # Save article to database
                        try:
                            Article.add_article(
                                db=db,
                                feed_id=feed.id,
                                url=article_url,
                                title=scraped_data['title'] or article_meta['title'],
                                author=scraped_data['author'] or article_meta.get('author'),
                                body=scraped_data['body'],
                                media_links='\n'.join(scraped_data['media_links']) if scraped_data['media_links'] else None,
                                published_at=article_meta.get('published_at'),
                            )
                            
                            stats['articles_scraped'] += 1
                            logger.info(f"Saved article: {article_url}")
                            
                        except ValueError as e:
                            # Duplicate detected during save (race condition)
                            logger.warning(f"Duplicate article detected during save: {e}")
                            stats['articles_duplicates'] += 1
                        
                except Exception as e:
                    logger.error(f"Error processing feed {feed.url}: {e}")
                    typer.echo(f"  → Error: {e}")
            
            # Display summary statistics
            typer.echo("\n" + "="*50)
            typer.echo("Fetch Summary:")
            typer.echo(f"  Feeds processed: {stats['feeds_processed']}")
            typer.echo(f"  Articles found: {stats['articles_found']}")
            typer.echo(f"  Articles scraped: {stats['articles_scraped']}")
            typer.echo(f"  Duplicates skipped: {stats['articles_duplicates']}")
            typer.echo(f"  Errors: {stats['articles_errors']}")
            typer.echo("="*50)
            
            logger.info("Fetch-all operation completed successfully")
            
    except Exception as e:
        logger.error(f"Error during fetch-all operation: {e}")
        typer.echo(f"Error: {e}")
        raise typer.Exit(1)

