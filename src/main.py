"""Main entry point for Geulmaru CLI application."""
import typer

from src.cli.init_db import init_db_command

# Create main CLI app
app = typer.Typer(help="Geulmaru - RSS Collector Application")


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

