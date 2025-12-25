# PowerShell-скрипт для запуска системы управления отелем

Write-Host "========================================" -ForegroundColor Green
Write-Host "Скрипт запуска системы управления отелем" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green

# Проверить, находимся ли мы в каталоге проекта
if (-not (Test-Path "manage.py")) {
    Write-Host "Ошибка: Файл manage.py не найден. Пожалуйста, запустите этот скрипт в корневом каталоге проекта." -ForegroundColor Red
    exit 1
}

# Проверить виртуальную среду
if (-not (Test-Path "venv")) {
    Write-Host "Создание виртуальной среды..." -ForegroundColor Yellow
    python -m venv venv
}

# Активировать виртуальную среду
Write-Host "Активация виртуальной среды..." -ForegroundColor Yellow
$env:Path = "venv\Scripts;" + $env:Path

# Установить переменные окружения Django
$env:DJANGO_SETTINGS_MODULE = "hotel_project.settings"

# Установить зависимости
Write-Host "Установка зависимостей..." -ForegroundColor Yellow
pip install -r requirements.txt

# Создать миграции
Write-Host "Создание миграций базы данных..." -ForegroundColor Yellow
python manage.py makemigrations

# Применить миграции
Write-Host "Применение миграций базы данных..." -ForegroundColor Yellow
python manage.py migrate

# Запустить сервер
Write-Host "Запуск сервера разработки..." -ForegroundColor Yellow
Write-Host "Сервер будет доступен по адресу http://127.0.0.1:8000/" -ForegroundColor Cyan
Write-Host "Нажмите Ctrl+C для остановки сервера" -ForegroundColor Cyan
python manage.py runserver