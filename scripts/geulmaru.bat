@echo off
REM RSS Collector (글마루) CLI 실행 스크립트 (Windows)

REM 스크립트 디렉토리 찾기
set SCRIPT_DIR=%~dp0
set PROJECT_ROOT=%SCRIPT_DIR%\..

REM 가상환경 경로
set VENV_DIR=%PROJECT_ROOT%\venv

REM 가상환경이 없으면 에러
if not exist "%VENV_DIR%" (
    echo ❌ 가상환경이 없습니다. 먼저 다음 명령어를 실행해주세요:
    echo    scripts\setup.bat
    exit /b 1
)

REM Python이 가상환경에 없으면 에러
if not exist "%VENV_DIR%\Scripts\python.exe" (
    echo ❌ 가상환경에 Python이 없습니다.
    echo    scripts\setup.bat를 다시 실행해주세요.
    exit /b 1
)

REM urllib3 경고 비활성화
set PYTHONWARNINGS=ignore

REM 명령어 인자가 없으면 도움말 표시
if "%1"=="" (
    call "%VENV_DIR%\Scripts\activate.bat"
    python -m src.main --help
    exit /b 0
)

REM 서브커맨드만 입력한 경우 자동으로 --help 추가
REM 예: feed -> feed --help, articles -> articles --help
if "%2"=="" (
    if "%1"=="feed" (
        call "%VENV_DIR%\Scripts范畴tivate.bat"
        python -m src.main %1 --help
        exit /b 0
    )
    if "%1"=="articles" (
        call "%VENV_DIR%\Scripts\activate.bat"
        python -m src.main %1 --help
        exit /b 0
    )
)

REM 가상환경 활성화 및 실행
call "%VENV_DIR%\Scripts\activate.bat"
python -m src.main %*

