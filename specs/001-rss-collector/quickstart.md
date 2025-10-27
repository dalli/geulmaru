# Quickstart: RSS Collector Application (글마루)

**Created**: 2025-01-21
**Feature**: RSS Collector Application

## Overview

Get started with the Geulmaru (글마루) RSS collector application in 5 minutes. This guide walks you through setting up and using the CLI to collect and archive news articles.

## Prerequisites

- Python 3.10 or later
- pip (Python package manager)

## Installation

### 1. Create Project Directory

```bash
mkdir geulmaru
cd geulmaru
```

### 2. Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # On macOS/Linux
# OR
venv\Scripts\activate    # On Windows
```

### 3. Install Dependencies

Create `requirements.txt`:

```text
typer==0.12.0
feedparser==6.0.11
newspaper3k==0.2.8
sqlalchemy==2.0.23
pytest==7.4.3
```

Install:

```bash
pip install -r requirements.txt
```

## Quick Start (5 Minutes)

### Step 1: Initialize Database

```bash
python main.py init-db
```

**Expected Output**:
```
Database initialized successfully at: ./geulmaru.db
```

### Step 2: Add RSS Feeds

Add some test RSS feeds:

```bash
python main.py feed add "https://www.hani.co.kr/rss/"
python main.py feed add "https://rss.joins.com/joins_news_list.xml"
```

**Expected Output**:
```
✅ Feed [ID: 1] registered: https://www.hani.co.kr/rss/
✅ Feed [ID: 2] registered: https://rss.joins.com/joins_news_list.xml
```

### Step 3: List Feeds

```bash
python main.py feed list
```

**Expected Output**:
```
ID | URL                                      | Created
---+------------------------------------------+------------------
2  | https://rss.joins.com/joins_news_list.xml| 2025-01-21 12:30
1  | https://www.hani.co.kr/rss/              | 2025-01-21 12:25
```

### Step 4: Fetch Articles

```bash
python main.py fetch-all
```

**Expected Output**:
```
🔄 [ID: 1] Processing feed: https://www.hani.co.kr/rss/
   -> [SAVE] New article: Article Title 1
   -> [SAVE] New article: Article Title 2
   -> [SKIP] Already exists: Article Title 3
🔄 [ID: 2] Processing feed: https://rss.joins.com/joins_news_list.xml
   -> [SAVE] New article: Another Article Title
✅ Collection complete: 3 new articles, 15 total articles
```

### Step 5: View Articles

```bash
python main.py articles list
```

**Expected Output**:
```
ID | Title                    | Author    | Feed                    | Saved
---+--------------------------+-----------+-------------------------+------------------
3  | Another Article Title    | Jane Doe  | joins.com/...xml        | 2025-01-21 12:35
2  | Article Title 2          | John Smith| hani.co.kr/rss         | 2025-01-21 12:32
1  | Article Title 1          | John Doe  | hani.co.kr/rss         | 2025-01-21 12:30
```

### Step 6: Search Articles

```bash
python main.py articles search "경제"
```

**Expected Output**:
```
Found 2 articles matching "경제":
ID | Title                    | Author    | Feed                    | Saved
---+--------------------------+-----------+-------------------------+------------------
5  | 한국 경제 성장률          | 한 기자    | joins.com/...xml        | 2025-01-21 12:33
2  | 경제 정책 분석            | 김 기자    | hani.co.kr/rss         | 2025-01-21 12:32
```

## Common Workflows

### Daily Collection Workflow

```bash
# Run once daily
python main.py fetch-all
```

### Add New Feed

```bash
python main.py feed add "https://new-feed.example.com/rss"
python main.py fetch-all  # Collect from new feed
```

### Remove Old Feed

```bash
python main.py feed list  # Find ID
python main.py feed remove 1  # Remove by ID
```

### View Recent Articles

```bash
# View last 10 articles (default)
python main.py articles list

# View last 50 articles
python main.py articles list --limit 50

# Search for specific topic
python main.py articles search "데이터베이스"
```

## Configuration

Set environment variables (optional):

```bash
# Change database location
export GEULMARU_DB_PATH=/path/to/custom.db

# Change log level (DEBUG, INFO, WARN, ERROR)
export GEULMARU_LOG_LEVEL=INFO

# Custom User-Agent for scraping
export GEULMARU_USER_AGENT="Mozilla/5.0 ..."

# Then run commands
python main.py fetch-all
```

## Troubleshooting

### Error: "Database not initialized"

```bash
python main.py init-db
```

### Error: "Feed URL already exists"

Feeds with the same URL cannot be added twice. Use `feed list` to find existing feed or remove and re-add.

### Error: "Network error during fetch"

- Check internet connection
- Verify RSS feed URL is accessible (open in browser)
- Check `GEULMARU_LOG_LEVEL=DEBUG` for detailed errors

### Error: "Scraping failed for some articles"

This is normal. Articles may have partial information (title, URL) saved even if scraping fails. Check logs with `GEULMARU_LOG_LEVEL=WARN`.

### No articles found after fetch-all

- Verify RSS feeds are active (open URL in browser)
- Check feed list: `python main.py feed list`
- Run with debug: `GEULMARU_LOG_LEVEL=DEBUG python main.py fetch-all`

## Next Steps

1. Add more RSS feeds to your collection
2. Set up automated collection (cron job or scheduler)
3. Explore the database directly: `sqlite3 geulmaru.db`
4. Customize User-Agent if scraping is blocked

## Help

Get help for any command:

```bash
python main.py --help
python main.py feed --help
python main.py articles --help
```

## Expected File Structure

After setup, your project should look like:

```text
geulmaru/
├── venv/                    # Virtual environment
├── src/
│   ├── models/              # Database models
│   ├── services/            # Business logic
│   ├── cli/                 # CLI commands
│   └── main.py              # Entry point
├── tests/                   # Test files
├── geulmaru.db              # SQLite database (created)
├── requirements.txt         # Dependencies
└── README.md                # Project documentation
```

## Performance Benchmarks

Target performance (from Success Criteria):

- Database initialization: < 2 seconds
- Add feed and list: < 5 seconds
- Fetch 50 articles: < 5 minutes
- View 100 articles: < 3 seconds
- Search keyword: < 2 seconds

## Learning Resources

- [Typer Documentation](https://typer.tiangolo.com/)
- [feedparser Documentation](https://pythonhosted.org/feedparser/)
- [newspaper3k Documentation](https://github.com/codelucas/newspaper)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)

## Support

For issues or questions:
- Check logs with `GEULMARU_LOG_LEVEL=DEBUG`
- Review constitution for design principles
- See `research.md` for technology decisions

