#!/bin/bash
# RSS Collector (글마루) 초기 설정 스크립트

set -e  # 에러 발생 시 즉시 종료

# 스크립트 디렉토리 찾기
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

echo "🚀 RSS Collector (글마루) 초기 설정을 시작합니다..."
echo ""

# 프로젝트 루트로 이동
cd "$PROJECT_ROOT"

# Python 버전 확인
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3가 설치되어 있지 않습니다."
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
echo "✅ Python 버전: $(python3 --version)"

# 가상환경 생성 (없는 경우)
if [ ! -d "venv" ]; then
    echo "📦 가상환경을 생성합니다..."
    python3 -m venv venv
    echo "✅ 가상환경이 생성되었습니다."
else
    echo "✅ 가상환경이 이미 존재합니다."
fi

# 가상환경 활성화
echo "🔧 가상환경을 활성화합니다..."
source venv/bin/activate

# pip 업그레이드
echo "📦 pip를 업그레이드합니다..."
pip install --upgrade pip > /dev/null 2>&1

# 의존성 설치
echo "📦 의존성 패키지를 설치합니다..."
pip install -r requirements.txt

echo ""
echo "✅ 초기 설정이 완료되었습니다!"
echo ""
echo "다음 명령어로 실행할 수 있습니다:"
echo "  ./scripts/geulmaru init-db"
echo ""
echo "또는 직접 실행:"
echo "  python -m src.main init-db"

