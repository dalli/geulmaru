@echo off
REM RSS Collector (글마루) 초기 설정 스크립트 (Windows)

setlocal enabledelayedexpansion

echo 🚀 RSS Collector (글마루) 초기 설정을 시작합니다...
echo.

REM 스크립트 디렉토리 찾기
set SCRIPT_DIR=%~dp0
set PROJECT_ROOT=%SCRIPT_DIR%\..

REM 프로젝트 루트로 이동
cd /d "%PROJECT_ROOT%"

REM Python 버전 확인
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python3가 설치되어 있지 않습니다.
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo ✅ Python 버전: !PYTHON_VERSION!

REM 가상환경 생성 (없는 경우)
if not exist "venv" (
    echo 📦 가상환경을 생성합니다...
    python -m venv venv
    echo ✅ 가상환경이 생성되었습니다.
) else (
    echo ✅ 가상환경이 이미 존재합니다.
)

REM 가상환경 활성화
echo 🔧 가상환경을 활성화합니다...
call venv\Scripts\activate.bat

REM pip 업그레이드
echo 📦 pip를 업그레이드합니다...
python -m pip install --upgrade pip >nul 2>&1

REM 의존성 설치
echo 📦 의존성 패키지를 설치합니다...
pip install -r requirements.txt

echo.
echo ✅ 초기 설정이 완료되었습니다!
echo.
echo 다음 명령어로 실행할 수 있습니다:
echo   scripts\geulmaru.bat init-db
echo.
echo 또는 직접 실행:
echo   python -m src.main init-db

endlocal

