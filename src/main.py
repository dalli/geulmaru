"""Main entry point for Geulmaru CLI application."""
import typer

from src.cli.init_db import init_db_command
from src.cli.feed import add_feed_command, list_feeds_command, remove_feed_command
from src.cli.fetch import fetch_all_command
from src.cli.articles import list_articles_command, search_articles_command

# Create main CLI app
app = typer.Typer(help="Geulmaru - RSS Collector Application")

# Create feed sub-app
feed_app = typer.Typer(help="Manage RSS feeds")
app.add_typer(feed_app, name="feed")

# Create articles sub-app
articles_app = typer.Typer(help="Manage collected articles")
app.add_typer(articles_app, name="articles")


@feed_app.command("add")
def add_feed(url: str = typer.Argument(..., help="RSS feed URL to add")):
    """Add a new RSS feed to the database."""
    add_feed_command(url)


@feed_app.command("list")
def list_feeds():
    """List all registered RSS feeds."""
    list_feeds_command()


@feed_app.command("remove")
def remove_feed(feed_id: int = typer.Argument(..., help="ID of the feed to remove")):
    """Remove a RSS feed from the database."""
    remove_feed_command(feed_id)


@app.command("init-db")
def init_db():
    """Initialize the database with necessary tables."""
    init_db_command()


@app.command("fetch-all")
def fetch_all():
    """Fetch articles from all registered RSS feeds."""
    fetch_all_command()


@articles_app.command("list")
def list_articles(limit: int = typer.Option(10, "--limit", "-l", help="Number of articles to display")):
    """List recent articles from the archive."""
    list_articles_command(limit)


@articles_app.command("search")
def search_articles(keyword: str = typer.Argument(..., help="Search keyword"), limit: int = typer.Option(50, "--limit", "-l", help="Number of results to display")):
    """Search articles containing a keyword in title or body."""
    search_articles_command(keyword, limit)


@app.command()
def version():
    """Show version information."""
    typer.echo("Geulmaru v0.1.0")


if __name__ == "__main__":
    app()

