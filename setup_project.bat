@echo off
echo Setting up Hotel Management System...

REM Check if we are in the project directory
if not exist manage.py (
    echo Error: manage.py not found. Please run this script from the project directory.
    pause
    exit /b 1
)

REM Create virtual environment
echo Creating virtual environment...
python -m venv venv

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt

REM Set Django environment variables
set DJANGO_SETTINGS_MODULE=hotel_project.settings

REM Create database migrations
echo Creating migrations...
python manage.py makemigrations

REM Apply migrations
echo Applying migrations...
python manage.py migrate

REM Ask if superuser should be created
echo.
echo Setup complete!
echo To create a superuser, run: python manage.py createsuperuser
echo To start the server, run: python manage.py runserver

pause