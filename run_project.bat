@echo off
echo Starting Hotel Management System...

REM Check if we are in the project directory
if not exist manage.py (
    echo Error: manage.py not found. Please run this script from the project directory.
    pause
    exit /b 1
)

REM Activate virtual environment (if exists)
if exist venv\Scripts\activate.bat (
    echo Activating virtual environment...
    call venv\Scripts\activate.bat
)

REM Set Django environment variables
set DJANGO_SETTINGS_MODULE=hotel_project.settings

REM Run Django development server
echo Starting development server...
echo The server will be available at http://127.0.0.1:8000/
echo Press Ctrl+C to stop the server
python manage.py runserver

pause