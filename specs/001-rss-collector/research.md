# Research: RSS Collector Application

**Created**: 2025-01-21
**Feature**: RSS Collector Application (글마루)

## Technology Decisions

### Typer for CLI Framework

**Decision**: Use Typer as the CLI framework for Python

**Rationale**:
- Modern, type-hint based framework for building CLI applications
- Automatic help generation from function signatures
- Built on Click for powerful command composition
- Excellent Python 3.10+ type hints support
- Simple syntax: `import typer; app = typer.Typer()`

**Alternatives Considered**:
- Click: Lower-level, more verbose syntax
- argparse: Standard library but verbose for complex CLIs
- docopt: Declarative but less Pythonic

### feedparser for RSS Parsing

**Decision**: Use feedparser library for RSS/Atom feed parsing

**Rationale**:
- Mature, widely-used library for RSS parsing in Python
- Handles multiple feed formats (RSS 2.0, Atom, RDF)
- Automatically extracts article metadata (title, URL, published date)
- Handles edge cases like malformed XML gracefully
- Simple API: `feed = feedparser.parse(url)`

**Alternatives Considered**:
- xml.etree.ElementTree: Low-level, requires manual parsing
- BeautifulSoup: Overkill for RSS, heavier dependency
- atoma: Newer but less mature than feedparser

### newspaper3k for Article Scraping

**Decision**: Use newspaper3k library for extracting article content from URLs

**Rationale**:
- Purpose-built for news article content extraction
- Extracts article body, author, images, videos automatically
- Handles JavaScript rendering for modern news sites
- Configurable User-Agent (important for avoiding bot blocking)
- Simple API: `article = Article(url); article.download(); article.parse()`

**Alternatives Considered**:
- BeautifulSoup + manual parsing: More control but much more code
- Selenium: Overkill for simple scraping, heavier dependency
- scrapy: Too complex for static article extraction

### SQLAlchemy for Database ORM

**Decision**: Use SQLAlchemy as the ORM for database operations

**Rationale**:
- Mature, well-documented ORM for Python
- Excellent SQLite support with declarative models
- Transaction management built-in (atomic operations)
- Migration support via Alembic
- Clear separation between models and queries

**Alternatives Considered**:
- peewee: Lighter but less feature-rich
- Django ORM: Too heavy for CLI app
- Raw SQL: Too verbose, error-prone

### SQLite for Storage

**Decision**: Use SQLite as the local database

**Rationale**:
- File-based, no server required (perfect for CLI app)
- Fast for read-heavy workloads
- ACID transactions (important for data integrity)
- Built-in in Python standard library
- Supports thousands of articles easily

**Alternatives Considered**:
- PostgreSQL: Overkill, requires server setup
- JSON files: No transactions, no query capability
- CSV files: No data integrity, no relationships

### pytest for Testing

**Decision**: Use pytest as the testing framework

**Rationale**:
- Widely adopted in Python ecosystem
- Fixtures for test data and mocks
- Clear assertion error messages
- Good integration with coverage tools
- Simple test discovery

**Alternatives Considered**:
- unittest: Standard library but more verbose
- nose: Deprecated in favor of pytest

## Design Patterns

### Modular Architecture

**Approach**: Separate concerns into independent modules

- **Models**: SQLAlchemy declarative models (`Feed`, `Article`)
- **Services**: Business logic (`feed_fetcher.py`, `feed_parser.py`, etc.)
- **CLI**: Typer commands for user interaction
- Each module independently testable with clear interfaces

### Error Handling Strategy

**Approach**: Fail gracefully without stopping entire process

- Network errors: Log and continue to next feed/article
- Parse errors: Skip malformed entries, log warning
- Scrape failures: Save partial data (title, URL), continue
- Database errors: Rollback transaction, log error
- All errors include context (URL, operation, timestamp)

### Logging Strategy

**Approach**: Structured logging with appropriate levels

- **DEBUG**: Detailed steps (parsing individual items)
- **INFO**: Progress updates (feed started, articles found)
- **WARN**: Recoverable issues (malformed XML, scrape failed)
- **ERROR**: Unrecoverable issues (database corruption)

Logging configuration via `GEULMARU_LOG_LEVEL` environment variable.

### Configuration Management

**Approach**: Environment variables for all configurable values

- `GEULMARU_DB_PATH`: Database file path (default: `./geulmaru.db`)
- `GEULMARU_USER_AGENT`: User-Agent string for scraping (default: standard browser UA)
- `GEULMARU_LOG_LEVEL`: Logging verbosity (default: INFO)

No hardcoded configuration in source code.

## Open Questions Resolved

### Q1: How to handle duplicate articles?

**Answer**: Use article `url` as unique identifier in database. Check for existing URL before scraping to avoid unnecessary work. URL-based deduplication is reliable since news articles have stable URLs.

### Q2: What if scraping fails for an article?

**Answer**: Save partial information from RSS feed (title, URL, published date) to database even if content scraping fails. This ensures articles aren't lost completely. Log error for user awareness.

### Q3: How to handle very large articles?

**Answer**: newspaper3k handles large articles efficiently. For database storage, SQLite TEXT fields handle up to 1GB. If article body exceeds practical limits, truncate with warning in log.

### Q4: Should I implement automatic scheduling?

**Answer**: Not in MVP. Initial version uses manual `fetch-all` command. Automatic scheduling with cron-like intervals is a future enhancement. Constitution requires it but allows manual scheduling initially.

## Assumptions

1. Users have internet connectivity when running `fetch-all`
2. SQLite database file is writable in current directory
3. Python 3.10+ environment available
4. RSS feeds are publicly accessible (no authentication)
5. Article pages are publicly accessible (no login required)

## Dependencies Summary

- **typer**: CLI framework
- **feedparser**: RSS parsing
- **newspaper3k**: Article scraping
- **sqlalchemy**: ORM and database operations
- **pytest**: Testing framework
- **requests**: HTTP requests (dependency of newspaper3k)

