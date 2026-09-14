@echo off
setlocal enabledelayedexpansion

:: Create venv if missing
if not exist "venv" (
    echo First-time setup: Creating virtual environment...
    python -m venv venv
)

:: Activate venv
call venv\Scripts\activate.bat

:: Install dependencies if needed
if exist "requirements.txt" (
    python3 -m pip install -q -r requirements.txt
)

:: Launch app
echo Launching MidleCode Studio...
python main\main.py

pause