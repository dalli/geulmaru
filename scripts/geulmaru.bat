@echo off
REM RSS Collector (글마루) CLI 실행 스크립트 (Windows)

REM 스크립트 디렉토리 찾기
set SCRIPT_DIR=%~dp0
set PROJECT_ROOT=%SCRIPT_DIR%\..

REM 가상환경 경로
set VENV_DIR=%PROJECT_ROOT%\venv

REM 가상환경이 없으면 에러
if not exist "%VENV_DIR%" (
    echo ❌ 가상환경이 없습니다. 먼저 setup.bat를 실행해주세요.
    exit /b 1
)

REM 가상환경 활성화 및 실행
call "%VENV_DIR%\Scripts\activate.bat"
python -m src.main %*

