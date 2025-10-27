# RSS Collector (글마루)

RSS Collector는 RSS 피드를 수집하고 아티클을 저장하는 CLI 애플리케이션입니다.

## 프로젝트 상태

현재 개발 초기 단계입니다. (Phase 3 완료 - Database Initialization)

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

### 2. 실행

**macOS/Linux:**
```bash
# 데이터베이스 초기화
./scripts/geulmaru init-db

# 또는 직접 실행
python -m src.main init-db
```

**Windows:**
```cmd
scripts\geulmaru.bat init-db
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

- ✅ Database Initialization (`init-db`) - 데이터베이스 초기화

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

# 커버리지 리포트
pytest --cov=src --cov-report=html
```

## 환경 변수

```bash
# 데이터베이스 경로 설정
export GEULMARU_DB_PATH="./custom/path/geulmaru.db"

# 로그 레벨 설정
export GEULMARU_LOG_LEVEL="DEBUG"

# 사용자 에이전트 설정
export GEULMARU_USER_AGENT="Custom User Agent"
```

## 라이선스

See LICENSE file.

