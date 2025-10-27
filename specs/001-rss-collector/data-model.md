# Data Model: RSS Collector Application

**Created**: 2025-01-21
**Feature**: RSS Collector Application (글마루)

## Overview

The application uses SQLite database with two main entities: **Feed** (RSS feed URLs) and **Article** (scraped articles). Both tables use integer primary keys and timestamps for tracking creation and publishing.

## Entities

### 1. Feed

Represents a registered RSS feed URL for article collection.

**Table**: `feeds`

**Fields**:
- `id` (Integer, Primary Key): Auto-incrementing unique identifier
- `url` (String, Unique, Not Null): RSS feed URL
- `created_at` (DateTime, Not Null): Timestamp of feed registration

**Relationships**:
- Has many `Article` records (one-to-many)
- Cascade delete: When feed is removed, associated articles remain (orphaned articles allowed)

**Validation Rules**:
- URL must be valid HTTP/HTTPS format
- URL must be unique (duplicate feeds rejected)
- URL should be a valid RSS feed (validated on add or fetch)

**State**:
- Normal state: Active and being monitored
- No state transitions (static entity)

### 2. Article

Represents a scraped news article with full content.

**Table**: `articles`

**Fields**:
- `id` (Integer, Primary Key): Auto-incrementing unique identifier
- `feed_id` (Integer, Foreign Key to `feeds.id`, Not Null): Source RSS feed
- `url` (String, Unique, Not Null): Original article URL (from RSS)
- `title` (String, Not Null): Article title (from RSS)
- `author` (String, Nullable): Author name (from scraped content)
- `body` (Text, Nullable): Full article body text (from scraped content)
- `media_links` (Text, Nullable): Newline-separated list of image/video URLs (from scraped content)
- `published_at` (DateTime, Nullable): Original publication timestamp (from RSS)
- `created_at` (DateTime, Not Null): Timestamp of article storage in database

**Relationships**:
- Belongs to one `Feed` (many-to-one via `feed_id`)
- Foreign key references `feeds.id`

**Validation Rules**:
- URL must be unique (duplicate articles rejected - FR-016)
- Title required (from RSS, always present)
- Author, body, media_links nullable (scraping may fail)
- If scraping fails, article still saved with RSS metadata (title, URL)
- `media_links` stored as newline-separated text or JSON array

**State**:
- Normal state: Successfully scraped with full content
- Partial state: Only RSS metadata available (scraping failed)
- No state transitions (static entity after creation)

## Database Schema

### feeds Table

```sql
CREATE TABLE feeds (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    url TEXT UNIQUE NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_feeds_url ON feeds(url);
```

### articles Table

```sql
CREATE TABLE articles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    feed_id INTEGER NOT NULL,
    url TEXT UNIQUE NOT NULL,
    title TEXT NOT NULL,
    author TEXT,
    body TEXT,
    media_links TEXT,
    published_at TIMESTAMP,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (feed_id) REFERENCES feeds(id)
);

CREATE INDEX idx_articles_feed_id ON articles(feed_id);
CREATE INDEX idx_articles_url ON articles(url);
CREATE INDEX idx_articles_published_at ON articles(published_at);
CREATE INDEX idx_articles_created_at ON articles(created_at);
```

**Indexes**:
- `idx_feeds_url`: Fast lookup by URL for duplicate prevention
- `idx_articles_feed_id`: Fast filtering by feed
- `idx_articles_url`: Fast lookup by URL for duplicate prevention
- `idx_articles_published_at`: Sorting articles by publication time
- `idx_articles_created_at`: Sorting articles by storage time

## Relationships Diagram

```
Feed (1) ───────< (many) Article

Feed:
  id: 1
  url: "https://example.com/rss"
  created_at: 2025-01-21 10:00:00

Article:
  id: 1
  feed_id: 1
  url: "https://example.com/article/123"
  title: "Example Article"
  author: "John Doe"
  body: "Full article text..."
  media_links: "https://example.com/img1.jpg\nhttps://example.com/img2.jpg"
  published_at: 2025-01-21 09:00:00
  created_at: 2025-01-21 10:05:00
```

## Data Flow

### 1. Feed Registration (feed add)

```text
User Input: feed add "https://example.com/rss"
  ↓
Validate URL format
  ↓
INSERT INTO feeds (url, created_at) VALUES (url, NOW())
  ↓
Return feed.id
```

### 2. Article Collection (fetch-all)

```text
For each feed:
  1. Fetch RSS XML → feed data
  2. Parse RSS → article metadata (title, url, published_at)
  3. For each article:
     a. CHECK: SELECT url FROM articles WHERE url = article.url
     b. IF NOT EXISTS:
        - Scrape URL → content (body, author, media_links)
        - INSERT INTO articles (feed_id, url, title, author, body, media_links, published_at, created_at)
     c. IF EXISTS:
        - Skip (duplicate prevention)
  4. Continue to next article
  5. Continue to next feed
```

### 3. Article Query (articles list/search)

```text
SELECT a.id, a.title, a.author, a.url, a.created_at, f.url as feed_url
FROM articles a
JOIN feeds f ON a.feed_id = f.id
WHERE [search conditions]
ORDER BY a.created_at DESC
LIMIT [limit]
```

## Constraints

### Uniqueness Constraints
- `feeds.url`: Unique (no duplicate RSS feeds)
- `articles.url`: Unique (no duplicate articles across all feeds)

### Foreign Key Constraints
- `articles.feed_id` → `feeds.id`: Cascade behavior TBD (currently allow orphaned articles)

### Not Null Constraints
- `feeds.url`: Required
- `feeds.created_at`: Required
- `articles.feed_id`: Required
- `articles.url`: Required
- `articles.title`: Required
- `articles.created_at`: Required

### Nullable Fields (Acceptable)
- `articles.author`: Author extraction may fail
- `articles.body`: Content scraping may fail
- `articles.media_links`: No media found
- `articles.published_at`: RSS may not provide date

## Data Integrity Rules

1. **Duplicate Prevention**: URL uniqueness enforced at database level (UNIQUE constraint)
2. **Atomic Transactions**: Each article save is one transaction (success or rollback)
3. **Partial Data Allowed**: Article can exist with only RSS metadata (title, URL)
4. **Orphaned Articles Allowed**: Articles remain in database if feed is deleted (for archive)
5. **Schema Versioning**: Initial schema version 1.0, future migrations via Alembic

## Migration Strategy

### Initial Schema (Version 1.0)

Created via `init-db` command:
1. Create `feeds` table with indexes
2. Create `articles` table with indexes
3. Set foreign key constraints

### Future Migrations

Use Alembic for schema versioning:
- Add columns (e.g., `updated_at`)
- Modify constraints (e.g., add NOT NULL to existing column)
- Add indexes
- Migrations are reversible

## Performance Considerations

### Read Patterns
- List recent articles: Index on `created_at` (descending)
- Search by keyword: Full-text search on `title` and `body`
- Filter by feed: Index on `feed_id`

### Write Patterns
- Bulk insert: Single transaction for multiple articles per feed
- Duplicate check: Index on `url` for fast lookup

### Storage Patterns
- TEXT fields sufficient for article bodies (SQLite handles 1GB per field)
- Indexes for frequently queried fields
- No partitioning needed (SQLite handles thousands of rows efficiently)

