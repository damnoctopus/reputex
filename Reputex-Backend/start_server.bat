@echo off
cd /d "%~dp0"

if exist ".venv\Scripts\activate.bat" (
    echo Activating virtual environment...
    call .venv\Scripts\activate.bat
) else (
    echo Warning: .venv not found. Make sure you have created the virtual environment.
)

echo Starting FastAPI server...
python -m uvicorn app.main:app --reload
