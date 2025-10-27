# RSS Collector (글마루)

RSS Collector는 RSS 피드를 수집하고 아티클을 저장하는 CLI 애플리케이션입니다.

## 프로젝트 상태

현재 개발 초기 단계입니다.

## 설치

```bash
# 가상 환경 생성
python3 -m venv venv
source venv/bin/activate  # Windows의 경우: venv\Scripts\activate

# 의존성 설치
pip install -r requirements.txt
```

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
pytest
```

## 라이선스

See LICENSE file.

