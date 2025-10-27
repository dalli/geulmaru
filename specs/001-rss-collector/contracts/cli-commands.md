# CLI Command Contracts: RSS Collector Application

**Created**: 2025-01-21
**Feature**: RSS Collector Application (글마루)

## Overview

This document defines the command-line interface contracts for the Geulmaru (글마루) RSS collector application. All commands follow Typer patterns with type hints and automatic help generation.

## Command Structure

### Entry Point

```python
# main.py
import typer

app = typer.Typer()

if __name__ == "__main__":
    app()
```

### Command Groups

- `geulmaru init-db` - Database initialization
- `geulmaru feed` - Feed management (add, list, remove)
- `geulmaru fetch-all` - Article collection
- `geulmaru articles` - Article viewing (list, search)

---

## 1. init-db

**Command**: `geulmaru init-db`

**Description**: Initialize SQLite database with required tables (feeds, articles).

**Usage**:
```bash
geulmaru init-db
```

**Parameters**: None

**Options**: None

**Returns**:
- Exit code 0: Success (database created or already exists)
- Exit code 1: Error (permission denied, invalid path)

**Output**:
- Success: "Database initialized successfully at: {db_path}"
- Error: "Error initializing database: {error_message}"

**Behavior**:
1. Create SQLite database file at `GEULMARU_DB_PATH` (default: `./geulmaru.db`)
2. Create `feeds` table with schema
3. Create `articles` table with schema
4. Create indexes
5. If database exists, skip (idempotent)

**Error Handling**:
- Permission denied: Log error, exit with code 1
- Disk full: Log error, exit with code 1
- Existing database: No error, skip creation

---

## 2. feed add

**Command**: `geulmaru feed add <url>`

**Description**: Register a new RSS feed URL for article collection.

**Usage**:
```bash
geulmaru feed add "https://example.com/rss"
```

**Parameters**:
- `url` (string, required): RSS feed URL

**Options**: None

**Returns**:
- Exit code 0: Success (feed registered)
- Exit code 1: Error (invalid URL, database error, duplicate)

**Output**:
- Success: "✅ Feed [ID: {id}] registered: {url}"
- Error: "❌ Error adding feed: {error_message}"

**Behavior**:
1. Validate URL format (HTTP/HTTPS)
2. Check for duplicate URL in database
3. Insert URL into `feeds` table
4. Return auto-generated feed ID
5. Display success message with ID and URL

**Error Handling**:
- Invalid URL format: Show validation error
- Duplicate URL: Optionally update existing feed or reject with error
- Database error: Log error, exit with code 1

---

## 3. feed list

**Command**: `geulmaru feed list`

**Description**: Display all registered RSS feeds with IDs.

**Usage**:
```bash
geulmaru feed list
```

**Parameters**: None

**Options**: None

**Returns**:
- Exit code 0: Success (feeds listed)
- Exit code 1: Error (database not initialized)

**Output**:
- Success (with feeds): Table format showing ID, URL, created_at
```
ID | URL                              | Created
---+----------------------------------+------------------
1  | https://example.com/rss           | 2025-01-21 10:00
2  | https://news.example.com/rss      | 2025-01-21 11:00
```
- Success (no feeds): "No feeds registered. Use 'feed add' to register a feed."
- Error: "Error listing feeds: {error_message}"

**Behavior**:
1. Query all feeds from `feeds` table
2. Sort by `created_at` (descending)
3. Format as table
4. Display message if no feeds exist

**Error Handling**:
- Database not initialized: Show error message
- Database error: Log error, exit with code 1

---

## 4. feed remove

**Command**: `geulmaru feed remove <id>`

**Description**: Remove a registered RSS feed by ID.

**Usage**:
```bash
geulmaru feed remove 1
```

**Parameters**:
- `id` (integer, required): Feed ID to remove

**Options**: None

**Returns**:
- Exit code 0: Success (feed removed)
- Exit code 1: Error (feed not found, database error)

**Output**:
- Success: "✅ Feed [ID: {id}] removed"
- Error (not found): "❌ Feed not found: {id}"
- Error (database): "❌ Error removing feed: {error_message}"

**Behavior**:
1. Check if feed exists by ID
2. Delete feed from `feeds` table
3. Associated articles remain in database (orphaned)
4. Display success message

**Error Handling**:
- Feed not found: Show error, exit with code 1
- Database error: Log error, exit with code 1

---

## 5. fetch-all

**Command**: `geulmaru fetch-all`

**Description**: Fetch and collect articles from all registered RSS feeds.

**Usage**:
```bash
geulmaru fetch-all
```

**Parameters**: None

**Options**: None

**Returns**:
- Exit code 0: Success (articles collected)
- Exit code 1: Error (database not initialized, critical failure)

**Output**:
- Progress (per feed): "🔄 [ID: {feed_id}] Processing feed..."
  - "   -> [SKIP] Already exists: {article_title}"
  - "   -> [SAVE] New article: {article_title}"
- Success: "✅ Collection complete: {new_count} new articles, {total_processed} total articles"
- Error: "❌ Error during collection: {error_message}"

**Behavior**:
1. Query all feeds from database
2. For each feed:
   a. Fetch RSS XML from URL
   b. Parse RSS entries
   c. For each article:
      - Check if URL exists in `articles` table
      - If not exists: Scrape article content
      - If scraping succeeds: Save full article
      - If scraping fails: Save partial article (title, URL only)
      - Log progress
   d. Continue to next feed (even on errors)
3. Display summary statistics

**Error Handling**:
- Network error: Log warning, continue to next feed
- Invalid RSS: Log warning, continue to next feed
- Scraping failure: Log warning, save partial, continue to next article
- Database error: Log error, exit with code 1 (critical)

**Performance**:
- Target: Process 50 articles in under 5 minutes (SC-008)
- Allow 95% success rate for scraped articles (SC-005)

---

## 6. articles list

**Command**: `geulmaru articles list [--limit=N]`

**Description**: Display recent articles from database.

**Usage**:
```bash
geulmaru articles list              # Default: 10 articles
geulmaru articles list --limit 50  # Show 50 articles
```

**Parameters**: None

**Options**:
- `--limit` (integer, optional): Number of articles to display (default: 10)

**Returns**:
- Exit code 0: Success (articles listed)
- Exit code 1: Error (database not initialized)

**Output**:
- Success (with articles): Table format
```
ID | Title                        | Author      | Feed            | Saved
---+------------------------------+-------------+-----------------+------------------
100| Example Article Title       | John Doe    | example.com/rss| 2025-01-21 12:00
99 | Another Article Title       | Jane Smith  | news.com/rss   | 2025-01-21 11:00
```
- Success (no articles): "No articles available. Run 'fetch-all' to collect articles."
- Error: "Error listing articles: {error_message}"

**Behavior**:
1. Query articles from `articles` table
2. Join with `feeds` table for feed URL
3. Sort by `created_at` (descending)
4. Limit results to N articles
5. Format as table with key fields

**Error Handling**:
- Database not initialized: Show error message
- Invalid limit: Validate (must be > 0, max 1000), show error

**Performance**:
- Target: Display 100 articles in under 3 seconds (SC-006)

---

## 7. articles search

**Command**: `geulmaru articles search <keyword>`

**Description**: Search articles by keyword in title or body.

**Usage**:
```bash
geulmaru articles search "데이터베이스"
```

**Parameters**:
- `keyword` (string, required): Search keyword

**Options**: None

**Returns**:
- Exit code 0: Success (articles found)
- Exit code 1: Error (database not initialized)

**Output**:
- Success (with results): Table format (same as list)
```
Found 5 articles matching "데이터베이스":
ID | Title                        | Author      | Feed            | Saved
---+------------------------------+-------------+-----------------+------------------
98 | Database Optimization Tips | John Doe    | tech.com/rss    | 2025-01-20 10:00
```
- Success (no results): "No articles found matching '{keyword}'"
- Error: "Error searching articles: {error_message}"

**Behavior**:
1. Search in `articles.title` and `articles.body` fields
2. Use SQL LIKE operator (case-insensitive)
3. Join with `feeds` table for feed URL
4. Sort by `created_at` (descending)
5. Display all matching articles

**Error Handling**:
- Database not initialized: Show error message
- Empty keyword: Validate (reject empty string), show error

**Performance**:
- Target: Return search results in under 2 seconds (SC-007)

---

## Environment Variables

All commands respect these environment variables:

- `GEULMARU_DB_PATH`: Database file path (default: `./geulmaru.db`)
- `GEULMARU_LOG_LEVEL`: Logging level - DEBUG, INFO, WARN, ERROR (default: INFO)
- `GEULMARU_USER_AGENT`: User-Agent string for scraping (default: Standard browser UA)

## Error Codes

- **0**: Success
- **1**: General error (database, network, validation)
- **2**: Configuration error (missing database, invalid environment)

## Help System

Typer automatically generates help for all commands:

```bash
geulmaru --help              # Show all commands
geulmaru feed --help         # Show feed subcommands
geulmaru articles --help     # Show articles subcommands
```

## Examples

```bash
# Initialize database
geulmaru init-db

# Add RSS feeds
geulmaru feed add "https://www.hani.co.kr/rss/"
geulmaru feed add "https://rss.joins.com/joins_news_list.xml"

# List feeds
geulmaru feed list

# Fetch articles
geulmaru fetch-all

# View articles
geulmaru articles list
geulmaru articles list --limit 20

# Search articles
geulmaru articles search "데이터베이스"
geulmaru articles search "AI"

# Remove feed
geulmaru feed remove 1
```

