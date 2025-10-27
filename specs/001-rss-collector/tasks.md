---
description: Task list for RSS Collector Application implementation
---

# Tasks: RSS Collector Application (글마루)

**Input**: Design documents from `/specs/001-rss-collector/`

**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: Tests are REQUIRED per constitution (Test-Driven Development). All user stories require unit and integration tests.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
- Paths shown below assume single project structure from plan.md

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 Create project structure (src/, tests/, requirements.txt)
- [x] T002 [P] Create Python virtual environment and install dependencies (typer, feedparser, newspaper3k, sqlalchemy, pytest)
- [x] T003 [P] Setup linting and formatting tools (black, ruff)
- [x] T004 [P] Configure pytest in tests/conftest.py
- [x] T005 [P] Create .gitignore with Python and database patterns

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T006 Setup environment configuration in src/config.py (GEULMARU_DB_PATH, GEULMARU_LOG_LEVEL, GEULMARU_USER_AGENT)
- [ ] T007 Create Feed model in src/models/feed.py
- [ ] T008 Create Article model in src/models/article.py
- [ ] T009 [P] Create database initialization in src/services/storage.py (create_tables function)
- [ ] T010 [P] Create logging configuration in src/config.py (structured logging with levels)
- [ ] T011 Create fixtures for test data in tests/fixtures/ (sample_rss.xml, sample_article.html)

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Database Initialization (Priority: P1) 🎯 MVP

**Goal**: User sets up the application for the first time by initializing the database with necessary tables

**Independent Test**: User runs `init-db` command and verifies that database file and tables are created successfully

### Tests for User Story 1

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [ ] T012 [P] [US1] Unit test for database initialization in tests/unit/test_storage.py
- [ ] T013 [P] [US1] Integration test for init-db command in tests/integration/test_init_db.py

### Implementation for User Story 1

- [ ] T014 [US1] Create init-db CLI command in src/cli/init_db.py
- [ ] T015 [US1] Implement database table creation with proper indexes in src/services/storage.py
- [ ] T016 [US1] Add database file path validation and error handling
- [ ] T017 [US1] Register init-db command in main.py
- [ ] T018 [US1] Add logging for database initialization operations

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Add RSS Feed (Priority: P1) 🎯 MVP

**Goal**: User registers a new RSS feed URL to the database for future collection

**Independent Test**: User runs `feed add <URL>` and verifies the feed is registered in the database

### Tests for User Story 2

- [ ] T019 [P] [US2] Unit test for Feed model in tests/unit/test_feed_model.py
- [ ] T020 [P] [US2] Unit test for URL validation in tests/unit/test_feed_model.py
- [ ] T021 [P] [US2] Integration test for feed add command in tests/integration/test_feed_add.py

### Implementation for User Story 2

- [ ] T022 [US2] Implement Feed.add_feed() method in src/models/feed.py
- [ ] T023 [US2] Add URL validation and duplicate checking in src/models/feed.py
- [ ] T024 [US2] Create feed CLI subcommand in src/cli/feed.py (add command)
- [ ] T025 [US2] Add error handling for invalid URLs and duplicates
- [ ] T026 [US2] Add logging for feed addition operations
- [ ] T027 [US2] Register feed subcommand in main.py

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - View Registered Feeds (Priority: P2)

**Goal**: User views all RSS feeds currently registered in the system

**Independent Test**: User runs `feed list` and sees all registered feeds with their IDs

### Tests for User Story 3

- [ ] T028 [P] [US3] Integration test for feed list command in tests/integration/test_feed_list.py

### Implementation for User Story 3

- [ ] T029 [US3] Implement Feed.list_all() method in src/models/feed.py
- [ ] T030 [US3] Create feed list CLI subcommand in src/cli/feed.py (list command)
- [ ] T031 [US3] Format feed list output with ID, URL, created_at columns
- [ ] T032 [US3] Handle empty feed list case with user-friendly message

---

## Phase 6: User Story 4 - Collect and Store Articles (Priority: P1) 🎯 MVP

**Goal**: User triggers article collection from all registered RSS feeds, fetching new articles, scraping their content, and storing them in the database

**Independent Test**: User runs `fetch-all` and verifies that new articles from registered feeds are collected, scraped, and saved to database

### Tests for User Story 4

- [ ] T033 [P] [US4] Unit test for RSS fetching in tests/unit/test_feed_fetcher.py
- [ ] T034 [P] [US4] Unit test for RSS parsing in tests/unit/test_feed_parser.py
- [ ] T035 [P] [US4] Unit test for article scraping in tests/unit/test_article_scraper.py
- [ ] T036 [P] [US4] Unit test for duplicate detection in tests/unit/test_storage.py
- [ ] T037 [P] [US4] Integration test for end-to-end fetch-all in tests/integration/test_fetch_all.py

### Implementation for User Story 4

- [ ] T038 [US4] Implement Feed Fetcher service in src/services/feed_fetcher.py (fetch RSS XML from URLs)
- [ ] T039 [US4] Implement Feed Parser service in src/services/feed_parser.py (parse XML to article metadata)
- [ ] T040 [US4] Implement Article Scraper service in src/services/article_scraper.py (extract content from URLs)
- [ ] T041 [US4] Implement article storage in src/services/storage.py (save articles with duplicate checking)
- [ ] T042 [US4] Implement duplicate detection by URL before scraping in src/services/storage.py
- [ ] T043 [US4] Add error handling for network failures and invalid RSS in src/services/feed_fetcher.py
- [ ] T044 [US4] Add error handling for scraping failures in src/services/article_scraper.py
- [ ] T045 [US4] Add logging for fetch progress and errors
- [ ] T046 [US4] Create fetch-all CLI command in src/cli/fetch.py
- [ ] T047 [US4] Register fetch command in main.py
- [ ] T048 [US4] Display summary statistics after fetch completion

**Checkpoint**: At this point, User Stories 1, 2, AND 4 should work together (core functionality)

---

## Phase 7: User Story 5 - View Collected Articles (Priority: P2)

**Goal**: User views recently collected articles from the archive

**Independent Test**: User runs `articles list` and sees recent articles with key information

### Tests for User Story 5

- [ ] T049 [P] [US5] Unit test for Article model in tests/unit/test_article_model.py
- [ ] T050 [P] [US5] Integration test for articles list command in tests/integration/test_articles_list.py

### Implementation for User Story 5

- [ ] T051 [US5] Implement Article.list_recent() method in src/models/article.py
- [ ] T052 [US5] Create articles list CLI subcommand in src/cli/articles.py (list command)
- [ ] T053 [US5] Add --limit option for number of articles to display
- [ ] T054 [US5] Format article list output with ID, title, author, feed, created_at
- [ ] T055 [US5] Join with Feed table to show feed URL
- [ ] T056 [US5] Handle empty article list case with user-friendly message
- [ ] T057 [US5] Register articles subcommand in main.py

**Checkpoint**: At this point, User Stories 1, 2, 4, AND 5 should work independently

---

## Phase 8: User Story 6 - Search Articles by Keyword (Priority: P3)

**Goal**: User searches for articles containing specific keywords in title or body

**Independent Test**: User runs `articles search "keyword"` and sees matching articles

### Tests for User Story 6

- [ ] T058 [P] [US6] Unit test for article search in tests/unit/test_article_model.py
- [ ] T059 [P] [US6] Integration test for articles search command in tests/integration/test_articles_search.py

### Implementation for User Story 6

- [ ] T060 [US6] Implement Article.search_by_keyword() method in src/models/article.py
- [ ] T061 [US6] Create articles search CLI subcommand in src/cli/articles.py (search command)
- [ ] T062 [US6] Implement SQL LIKE search on title and body fields
- [ ] T063 [US6] Format search results with same structure as list command
- [ ] T064 [US6] Handle "no results found" case with user-friendly message

---

## Phase 9: User Story 7 - Remove RSS Feed (Priority: P3)

**Goal**: User removes a registered RSS feed from the system

**Independent Test**: User runs `feed remove <ID>` and verifies the feed is removed from the list

### Tests for User Story 7

- [ ] T065 [P] [US7] Integration test for feed remove command in tests/integration/test_feed_remove.py

### Implementation for User Story 7

- [ ] T066 [US7] Implement Feed.remove_feed() method in src/models/feed.py
- [ ] T067 [US7] Create feed remove CLI subcommand in src/cli/feed.py (remove command)
- [ ] T068 [US7] Add error handling for non-existent feed ID
- [ ] T069 [US7] Add confirmation logging for feed removal

**Checkpoint**: All user stories should now be independently functional

---

## Phase 10: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T070 [P] Add retry logic for transient network failures in src/services/feed_fetcher.py
- [ ] T071 [P] Add graceful shutdown handler (SIGINT/SIGTERM) in main.py
- [ ] T072 [P] Improve logging with structured format and context
- [ ] T073 [P] Add performance optimization for large article lists
- [ ] T074 [P] Add README.md with installation and usage instructions
- [ ] T075 [P] Run quickstart.md validation
- [ ] T076 Add cleanup for orphaned articles (optional feature)
- [ ] T077 Code cleanup and refactoring

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-9)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Polish (Phase 10)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P1)**: Can start after Foundational (Phase 2) - Requires User Story 1 for database existence
- **User Story 3 (P2)**: Can start after User Story 2 - Requires feeds table to exist
- **User Story 4 (P1)**: Can start after User Stories 1 and 2 - Requires feeds table and Feed model
- **User Story 5 (P2)**: Can start after User Story 4 - Requires articles table to have data
- **User Story 6 (P3)**: Can start after User Story 4 - Requires articles table to have data
- **User Story 7 (P3)**: Can start after User Story 2 - Requires feeds table

### Within Each User Story

- Tests (REQUIRED) MUST be written and FAIL before implementation
- Models before services
- Services before CLI commands
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, test tasks for different stories can run in parallel
- Different user stories can be worked on in parallel by different team members (with dependencies respected)
- All tests for a user story marked [P] can run in parallel

---

## Parallel Example: User Story 1

```bash
# Launch tests for User Story 1 together:
Task: "Unit test for database initialization in tests/unit/test_storage.py"
Task: "Integration test for init-db command in tests/integration/test_init_db.py"
```

---

## Implementation Strategy

### MVP First (User Stories 1, 2, 4)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1 (Database Initialization)
4. Complete Phase 4: User Story 2 (Add RSS Feed)
5. Complete Phase 6: User Story 4 (Collect Articles)
6. **STOP and VALIDATE**: Test core functionality
7. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Validates DB setup
3. Add User Story 2 → Test independently → Validate feed management
4. Add User Story 4 → Test independently → Validate core collection (MVP!)
5. Add User Story 5 → Test independently → Validate article viewing
6. Add User Stories 3, 6, 7 → Test independently → Validate complete feature

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Stories 1 and 2 (Foundation + Feed CRUD)
   - Developer B: User Story 4 (Collection core) - after stories 1,2
   - Developer C: User Stories 3, 5, 6, 7 (Query features)
3. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence