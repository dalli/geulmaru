"""Main entry point for Geulmaru CLI application."""
import typer

from src.cli.init_db import init_db_command
from src.cli.feed import add_feed_command, list_feeds_command, remove_feed_command

# Create main CLI app
app = typer.Typer(help="Geulmaru - RSS Collector Application")

# Create feed sub-app
feed_app = typer.Typer(help="Manage RSS feeds")
app.add_typer(feed_app, name="feed")


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


@app.command()
def version():
    """Show version information."""
    typer.echo("Geulmaru v0.1.0")


if __name__ == "__main__":
    app()

