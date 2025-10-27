# RSS Collector (글마루)

RSS Collector는 RSS 피드를 수집하고 아티클을 저장하는 CLI 애플리케이션입니다.

## 프로젝트 상태

✅ 현재 모든 주요 기능이 완료되었습니다. (Phase 1-9 완료)

## 빠른 시작

### 1. 초기 설정

**macOS/Linux:**
```bash
./scripts/setup.sh
```

**Windows:**
```cmd
scripts\setup.bat
```

### 2. 데이터베이스 초기화

**macOS/Linux:**
```bash
./scripts/geulmaru init-db
```

**Windows:**
```cmd
scripts\geulmaru.bat init-db
```

### 3. 사용 방법

#### RSS 피드 추가
```bash
./scripts/geulmaru feed add "https://www.hani.co.kr/rss/"
./scripts/geulmaru feed add "https://rss.joins.com/joins_news_list.xml"
```

#### 피드 목록 보기
```bash
./scripts/geulmaru feed list
```

#### 아티클 수집
```bash
./scripts/geulmaru fetch-all
```

#### 아티클 목록 보기
```bash
./scripts/geulmaru articles list --limit 20
```

#### 아티클 검색
```bash
./scripts/geulmaru articles search "경제"
```

#### 피드 제거
```bash
./scripts/geulmaru feed remove 1
```

## 수동 설치

```bash
# 가상 환경 생성
python3 -m venv venv
source venv/bin/activate  # Windows의 경우: venv\Scripts\activate

# 의존성 설치
pip install -r requirements.txt
```

## 주요 기능

모든 사용자 스토리가 구현되었습니다:

- ✅ Database Initialization (`init-db`) - 데이터베이스 초기화
- ✅ Feed Management (`feed add/list/remove`) - RSS 피드 관리
- ✅ Article Collection (`fetch-all`) - 아티클 수집 및 스크래핑
- ✅ Article Viewing (`articles list`) - 아티클 목록 보기
- ✅ Article Search (`articles search`) - 키워드 검색
- ✅ Graceful Shutdown - 신호 핸들링 (SIGINT/SIGTERM)
- ✅ Retry Logic - 네트워크 실패 시 자동 재시도

## 개발

### 코드 포매팅

```bash
black src/ tests/
```

### 린팅

```bash
ruff check src/ tests/
```

### 테스트 실행

```bash
# 모든 테스트
pytest

# Unit 테스트만
pytest tests/unit/

# Integration 테스트만
pytest tests/integration/

# 특정 테스트 실행
pytest tests/integration/test_fetch_all.py -v

# 커버리지 리포트
pytest --cov=src --cov-report=html
```

테스트 커버리지를 보려면:
```bash
open htmlcov/index.html  # macOS
xdg-open htmlcov/index.html  # Linux
```

## 환경 변수

```bash
# 데이터베이스 경로 설정 (기본값: ./geulmaru.db)
export GEULMARU_DB_PATH="./custom/path/geulmaru.db"

# 로그 레벨 설정 (DEBUG, INFO, WARNING, ERROR, CRITICAL)
export GEULMARU_LOG_LEVEL="INFO"

# 사용자 에이전트 설정 (웹 스크래핑 시 사용)
export GEULMARU_USER_AGENT="Custom User Agent"

# 사용 예시
GEULMARU_LOG_LEVEL=DEBUG ./scripts/geulmaru fetch-all
```

## 아키텍처

```
src/
├── models/        # Database models (Feed, Article)
├── services/      # Business logic (Feed Fetcher, Parser, Scraper, Storage)
├── cli/          # CLI command implementations
├── config.py     # Configuration and environment variables
└── main.py       # Entry point and CLI setup

tests/
├── unit/         # Unit tests for individual components
├── integration/  # Integration tests for CLI commands
└── fixtures/     # Test data (sample RSS XML, HTML)
```

## 주요 기능 상세

### 1. RSS 피드 관리
- 피드 추가: URL 검증 및 중복 체크
- 피드 목록: 등록된 모든 피드 조회
- 피드 제거: ID 기반 삭제

### 2. 아티클 수집
- RSS 피드에서 최신 아티클 가져오기
- HTML 콘텐츠 스크래핑 (title, author, body, media)
- 중복 체크 (URL 기반)
- 네트워크 오류 시 자동 재시도 (3회)
- Graceful shutdown 지원 (Ctrl+C)

### 3. 아티클 검색
- 제목과 본문에서 키워드 검색
- SQL LIKE 검색 지원
- 검색 결과 제한 (기본 50개)

## 성능

- 데이터베이스 초기화: < 2초
- 피드 추가/목록: < 5초
- 50개 아티클 수집: < 5분
- 100개 아티클 조회: < 3초
- 키워드 검색: < 2초

## 문제 해결

**"Database not initialized" 에러:**
```bash
./scripts/geulmaru init-db
```

**네트워크 타임아웃:**
- 자동 재시도 기능이 있으므로 대기하거나 다시 시도하세요
- `GEULMARU_LOG_LEVEL=DEBUG`로 상세 로그 확인

**스크래핑 실패:**
- 일부 웹사이트는 봇 차단을 할 수 있습니다
- `GEULMARU_USER_AGENT` 환경 변수로 사용자 에이전트 변경

## 라이선스

See LICENSE file.

