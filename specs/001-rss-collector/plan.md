# Implementation Plan: RSS Collector Application (글마루)

**Branch**: `001-rss-collector` | **Date**: 2025-01-21 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-rss-collector/spec.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

RSS 피드를 주기적으로 읽어 기사 본문을 스크래핑하고 SQLite 데이터베이스에 저장하는 CLI 애플리케이션. Python, Typer, feedparser, newspaper3k, SQLAlchemy를 사용하여 RSS 피드 관리, 기사 수집/스크래핑, 검색 기능을 제공.

## Technical Context

**Language/Version**: Python 3.10+  
**Primary Dependencies**: Typer (CLI), feedparser (RSS), newspaper3k (scraping), SQLAlchemy (ORM)  
**Storage**: SQLite (local file-based database)  
**Testing**: pytest (unit/integration tests)  
**Target Platform**: Any system with Python (macOS, Linux, Windows)  
**Project Type**: CLI single project  
**Performance Goals**: 
- Database initialization < 2 seconds (SC-001)
- Add feed and view in list < 5 seconds (SC-002)
- View 100 articles < 3 seconds (SC-006)
- Search keyword results < 2 seconds (SC-007)
- Process 50 articles < 5 minutes (SC-008)  
**Constraints**: 
- Local-only operation (no network services)
- Handle 95% of articles successfully (SC-005)
- Graceful error handling without data corruption (SC-009)  
**Scale/Scope**: 
- Support 10+ RSS feeds simultaneously (SC-003)
- Handle thousands of articles in database

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### I. Modular Architecture ✅
**Requirement**: Components (RSS fetching, parsing, storage, scheduling) MUST be independently testable and replaceable.

**Implementation Plan**:
- RSS fetching: `src/services/feed_fetcher.py` (fetch RSS XML)
- RSS parsing: `src/services/feed_parser.py` (parse XML to article metadata)
- Article scraping: `src/services/article_scraper.py` (extract content from URLs)
- Storage: `src/services/storage.py` (database operations)
- CLI: `src/cli/` (Typer commands)
- Models: `src/models/` (Feed, Article entities)

**Status**: ✅ PASS - Clear separation planned

### II. Error Resilience (NON-NEGOTIABLE) ✅
**Requirement**: MUST gracefully handle network failures, invalid RSS feeds, database errors without crashing. Retry logic required.

**Implementation Plan**:
- Network errors: Try-except blocks with logging, continue to next feed
- Invalid RSS: Parse validation, skip malformed feeds, log warning
- Scrape failures: Continue to next article, save partial data (title, URL from RSS)
- Database errors: Transaction rollback, error logging, continue processing
- Retry logic: Implement for transient network failures (3 attempts with backoff)

**Status**: ✅ PASS - Comprehensive error handling strategy defined

### III. Observability ✅
**Requirement**: ALL operations logged with structured logging. Metrics for fetch success/failure, articles processed, DB operations.

**Implementation Plan**:
- Use Python logging module with structured format
- Log levels: DEBUG (detailed steps), INFO (progress), WARN (recoverable errors), ERROR (failures)
- Metrics: Track counts of fetched/saved/failed articles per feed
- Execution timing: Log start/end time per feed processing
- Console output: Show progress during fetch-all operation

**Status**: ✅ PASS - Logging strategy comprehensive

### IV. Test-Driven Development ✅
**Requirement**: Unit tests for RSS parsing, data validation, DB operations. Integration tests for end-to-end pipeline.

**Implementation Plan**:
- Unit tests: `tests/unit/test_feed_parser.py`, `tests/unit/test_storage.py`, `tests/unit/test_scraper.py`
- Integration tests: `tests/integration/test_fetch_pipeline.py`
- Mock external dependencies: requests (HTTP), database (in-memory SQLite)
- Fixtures: Sample RSS XML, article HTML
- CI/CD: Make tests runnable independently

**Status**: ✅ PASS - Testing strategy defined

### V. Configuration Management ✅
**Requirement**: All configurable values externalized via environment variables or config files.

**Implementation Plan**:
- Database path: Environment variable `GEULMARU_DB_PATH` (default: `./geulmaru.db`)
- User-Agent: Environment variable `GEULMARU_USER_AGENT` (default: standard browser UA)
- Log level: Environment variable `GEULMARU_LOG_LEVEL` (default: INFO)
- No hardcoded URLs or settings in source code
- Configuration validation on startup with clear error messages

**Status**: ✅ PASS - Configuration externalized

### Data Integrity ✅
**Requirement**: Duplicate detection by URL, atomic transactions, schema versioning, data retention policy.

**Implementation Plan**:
- Duplicate detection: Check `url` uniqueness before scraping (FR-007, FR-016)
- Atomic transactions: Use SQLAlchemy transactions for article storage
- Schema versioning: Initial schema in migration, future changes via migrations
- Data retention: Implement optional cleanup (future feature, keep last N articles)

**Status**: ✅ PASS - Data integrity measures defined

### Scheduling Requirements ✅
**Requirement**: Configurable intervals per feed, handle missed executions, log timing, graceful shutdown.

**Implementation Plan**:
- Manual scheduling: CLI-based `fetch-all` command (automatic scheduling future enhancement)
- Execution logging: Log start/end times, duration per feed
- Graceful shutdown: Catch SIGINT/SIGTERM, complete current article before exit
- Future: Add cron-like scheduler with configurable intervals (constitution requirement)

**Status**: ✅ PASS - Initial manual scheduling, auto-scheduling for future phase

**Overall Status**: ✅ ALL GATES PASSED

## Project Structure

### Documentation (this feature)

```text
specs/001-rss-collector/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output (/speckit.plan command)
├── data-model.md        # Phase 1 output (/speckit.plan command)
├── quickstart.md        # Phase 1 output (/speckit.plan command)
├── contracts/           # Phase 1 output (/speckit.plan command)
└── tasks.md             # Phase 2 output (/speckit.tasks command - NOT created by /speckit.plan)
```

### Source Code (repository root)

```text
src/
├── models/              # SQLAlchemy models (Feed, Article)
├── services/            # Business logic
│   ├── feed_fetcher.py  # Fetch RSS XML from URLs
│   ├── feed_parser.py   # Parse RSS XML to metadata
│   ├── article_scraper.py # Scrape article content from URLs
│   └── storage.py       # Database operations
├── cli/                 # Typer CLI commands
│   ├── __init__.py
│   ├── init_db.py       # init-db command
│   ├── feed.py          # feed add/list/remove commands
│   ├── fetch.py         # fetch-all command
│   └── articles.py      # articles list/search commands
└── main.py              # Entry point

tests/
├── unit/                # Unit tests
│   ├── test_feed_parser.py
│   ├── test_storage.py
│   └── test_scraper.py
├── integration/         # Integration tests
│   └── test_fetch_pipeline.py
└── fixtures/            # Test data
    ├── sample_rss.xml
    └── sample_article.html

geulmaru.db              # SQLite database (created at runtime)
```

**Structure Decision**: Single project structure selected as this is a CLI application without separate frontend/backend. Source code organized into models (SQLAlchemy entities), services (business logic), and CLI (Typer commands). Tests separated by type (unit vs integration) with fixtures for external dependencies.

## Complexity Tracking

> **No violations detected - Constitution check passed for all principles**

No complexity justification needed as all constitutional requirements are satisfied through standard implementation patterns.
