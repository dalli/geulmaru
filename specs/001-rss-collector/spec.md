# Feature Specification: RSS Collector Application (글마루)

**Feature Branch**: `001-rss-collector`
**Created**: 2025-01-21
**Status**: Draft
**Input**: User description: "RSS 피드를 주기적으로 읽어, 각 기사의 원문 URL에 접속해 본문 내용을 스크래핑(Scraping)합니다. 추출된 핵심 정보(제목, 기자, 본문, 미디어 링크)를 로컬 데이터베이스에 저장하여 개인화된 뉴스 아카이브를 구축하는 CLI(Command Line Interface) 애플리케이션입니다."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Database Initialization (Priority: P1)

**Journey**: User sets up the application for the first time by initializing the database with necessary tables.

**Why this priority**: This is the foundation that all other features depend on. Without database initialization, no other operations are possible.

**Independent Test**: User runs `init-db` command and verifies that database file and tables are created successfully. This delivers the basic infrastructure for the application.

**Acceptance Scenarios**:

1. **Given** user has Python environment ready, **When** user runs `init-db` command, **Then** system creates SQLite database file with `feeds` and `articles` tables
2. **Given** database already exists, **When** user runs `init-db` again, **Then** system either skips creation or safely overwrites/resets the database without losing data
3. **Given** user has no write permissions, **When** user runs `init-db`, **Then** system displays error message explaining permission issue

---

### User Story 2 - Add RSS Feed (Priority: P1)

**Journey**: User registers a new RSS feed URL to the database for future collection.

**Why this priority**: Users need to register feeds before collecting articles. This is the primary way to configure what content will be collected.

**Independent Test**: User runs `feed add <URL>` and verifies the feed is registered in the database. This delivers the ability to configure content sources.

**Acceptance Scenarios**:

1. **Given** database is initialized, **When** user runs `feed add "https://example.com/rss"`, **Then** system saves the RSS URL to database and confirms registration
2. **Given** feed URL already exists, **When** user tries to add duplicate URL, **Then** system either prevents duplicate or updates existing record with timestamp
3. **Given** invalid URL format, **When** user runs `feed add "invalid-url"`, **Then** system displays validation error message
4. **Given** URL is unreachable, **When** user adds invalid RSS URL, **Then** system either warns or attempts basic validation before saving

---

### User Story 3 - View Registered Feeds (Priority: P2)

**Journey**: User views all RSS feeds currently registered in the system.

**Why this priority**: Users need to verify which feeds are configured and identify feeds by their database ID for management operations.

**Independent Test**: User runs `feed list` and sees all registered feeds with their IDs. This delivers feed management visibility.

**Acceptance Scenarios**:

1. **Given** database has registered feeds, **When** user runs `feed list`, **Then** system displays all feeds with their ID, URL, and registration timestamp
2. **Given** no feeds registered, **When** user runs `feed list`, **Then** system displays message indicating no feeds are registered
3. **Given** many feeds (100+), **When** user runs `feed list`, **Then** system displays all feeds or implements pagination

---

### User Story 4 - Collect and Store Articles (Priority: P1)

**Journey**: User triggers article collection from all registered RSS feeds, fetching new articles, scraping their content, and storing them in the database.

**Why this priority**: This is the core functionality of the application - collecting and archiving articles. Without this, the application provides no value.

**Independent Test**: User runs `fetch-all` and verifies that new articles from registered feeds are collected, scraped, and saved to database. This delivers the primary value of article archiving.

**Acceptance Scenarios**:

1. **Given** feeds are registered, **When** user runs `fetch-all`, **Then** system fetches each RSS feed, parses entries, checks for duplicates by URL, scrapes new articles, and saves them to database
2. **Given** article already exists in database, **When** system encounters duplicate URL, **Then** system skips that article and continues with next article
3. **Given** RSS feed is temporarily unavailable, **When** fetch-all encounters network error, **Then** system logs error for that feed and continues with other feeds
4. **Given** article page cannot be scraped, **When** scrape fails for an article, **Then** system logs error, saves partial information (title, URL from RSS), and continues with next article
5. **Given** successful collection, **When** fetch-all completes, **Then** system displays summary of total articles processed and newly added articles

---

### User Story 5 - View Collected Articles (Priority: P2)

**Journey**: User views recently collected articles from the archive.

**Why this priority**: Users need to access the collected articles to verify successful collection and review content.

**Independent Test**: User runs `articles list` and sees recent articles with key information. This delivers article browsing capability.

**Acceptance Scenarios**:

1. **Given** articles exist in database, **When** user runs `articles list`, **Then** system displays recent 10 articles with title, source, and storage time
2. **Given** user wants more articles, **When** user runs `articles list --limit 50`, **Then** system displays 50 recent articles
3. **Given** no articles collected, **When** user runs `articles list`, **Then** system displays message indicating no articles available

---

### User Story 6 - Search Articles by Keyword (Priority: P3)

**Journey**: User searches for articles containing specific keywords in title or body.

**Why this priority**: As the archive grows, users need to find specific content quickly through search functionality.

**Independent Test**: User runs `articles search "keyword"` and sees matching articles. This delivers content discovery capability.

**Acceptance Scenarios**:

1. **Given** articles contain keyword, **When** user runs `articles search "데이터베이스"`, **Then** system displays all articles where title or body contains the keyword
2. **Given** keyword not found, **When** user searches non-existent term, **Then** system displays message indicating no matches found
3. **Given** keyword matches multiple articles, **When** user searches common term, **Then** system displays all matching articles with pagination if needed

---

### User Story 7 - Remove RSS Feed (Priority: P3)

**Journey**: User removes a registered RSS feed from the system.

**Why this priority**: Users need to manage their feed subscriptions, removing feeds they no longer want to track.

**Independent Test**: User runs `feed remove <ID>` and verifies the feed is removed from the list. This delivers feed management capability.

**Acceptance Scenarios**:

1. **Given** feed with ID 1 exists, **When** user runs `feed remove 1`, **Then** system removes that feed from database
2. **Given** non-existent feed ID, **When** user runs `feed remove 999`, **Then** system displays error message indicating feed not found
3. **Given** feed is removed, **When** user runs `feed list`, **Then** removed feed no longer appears in the list

---

### Edge Cases

- What happens when RSS feed contains invalid XML?
- How does system handle articles with missing information (e.g., no author)?
- What if newspaper3k cannot extract body text from some pages?
- How does system handle articles with very large body text (performance)?
- What happens when duplicate URLs exist in different RSS feeds?
- How does system behave when disk space is full during article storage?
- What if RSS feed updates but provides malformed article URLs?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST initialize database with `feeds` and `articles` tables via `init-db` command
- **FR-002**: System MUST allow users to add RSS feed URLs to database via `feed add <URL>` command
- **FR-003**: System MUST allow users to list all registered RSS feeds via `feed list` command
- **FR-004**: System MUST allow users to remove RSS feeds by ID via `feed remove <ID>` command
- **FR-005**: System MUST fetch all registered RSS feeds when `fetch-all` command is executed
- **FR-006**: System MUST parse RSS XML to extract article metadata (title, URL, published date)
- **FR-007**: System MUST check for duplicate articles by comparing article URLs before scraping
- **FR-008**: System MUST scrape full article content from original URLs using content extraction
- **FR-009**: System MUST extract article information: body text, author, and media links
- **FR-010**: System MUST save scraped articles to database with all available metadata
- **FR-011**: System MUST continue processing remaining articles if one article fails during scraping
- **FR-012**: System MUST log errors for failed article scrapes without stopping the entire process
- **FR-013**: System MUST display list of recent articles via `articles list` command with optional limit
- **FR-014**: System MUST allow article search by keyword in title or body via `articles search <KEYWORD>` command
- **FR-015**: System MUST display article title, source feed, author, and storage timestamp for each article
- **FR-016**: System MUST prevent duplicate article storage by checking URL uniqueness in database

### Key Entities *(include if feature involves data)*

- **Feed**: Represents a registered RSS feed URL. Attributes: ID, URL, created_at timestamp. Relationship: has many articles.
- **Article**: Represents a scraped news article. Attributes: ID, feed_id, url (unique), title, author, body (full text), media_links, published_at (from RSS), created_at (storage time). Relationship: belongs to one feed.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can initialize database in under 2 seconds
- **SC-002**: Users can add RSS feed and view it in feed list within 5 seconds
- **SC-003**: System can successfully collect and store articles from at least 10 different RSS feeds
- **SC-004**: System avoids duplicate article storage by checking URL before scraping
- **SC-005**: System handles at least 95% of scraped articles without failures (5% failure tolerance)
- **SC-006**: Users can view 100 recent articles in under 3 seconds
- **SC-007**: Users can search articles by keyword and receive results in under 2 seconds
- **SC-008**: System can process and store 50 new articles in under 5 minutes
- **SC-009**: All operations complete without corrupting database or losing existing data
- **SC-010**: Failed scrapes do not prevent successful scrapes from completing
