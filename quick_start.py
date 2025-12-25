#!/usr/bin/env python
"""
Скрипт быстрого запуска для системы управления отелем
"""

import os
import sys
import subprocess
import venv

def check_python():
    """Проверить версию Python"""
    print("Проверка версии Python...")
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("Ошибка: Требуется Python 3.8 или выше")
        return False
    print(f"Версия Python: {version.major}.{version.minor}.{version.micro}")
    return True

def create_virtual_environment():
    """Создать виртуальную среду"""
    print("Создание виртуальной среды...")
    try:
        venv.create('venv', with_pip=True)
        print("Виртуальная среда создана успешно")
        return True
    except Exception as e:
        print(f"Ошибка: Не удалось создать виртуальную среду: {e}")
        return False

def activate_virtual_environment():
    """Активировать виртуальную среду"""
    print("Активация виртуальной среды...")
    # В Windows нам нужно запускать последующие команды в одной оболочке
    # Здесь мы просто уведомляем пользователя о необходимости активации среды
    if os.name == 'nt':  # Windows
        activate_script = os.path.join('venv', 'Scripts', 'activate.bat')
        if os.path.exists(activate_script):
            print(f"Пожалуйста, вручную выполните следующую команду для активации среды:")
            print(f"{activate_script}")
            return True
        else:
            print("Ошибка: Скрипт активации виртуальной среды не найден")
            return False
    else:  # Unix/Linux/Mac
        activate_script = os.path.join('venv', 'bin', 'activate')
        if os.path.exists(activate_script):
            print(f"Пожалуйста, вручную выполните следующую команду для активации среды:")
            print(f"source {activate_script}")
            return True
        else:
            print("Ошибка: Скрипт активации виртуальной среды не найден")
            return False

def install_requirements():
    """Установить зависимости проекта"""
    print("Установка зависимостей проекта...")
    try:
        # Используем python -m pip чтобы убедиться, что установка происходит в правильной среде
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("Зависимости установлены успешно")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Ошибка: Не удалось установить зависимости: {e}")
        return False

def create_migrations():
    """Создать миграции базы данных"""
    print("Создание миграций базы данных...")
    try:
        # Установить переменные окружения чтобы Django мог найти модуль настроек
        env = os.environ.copy()
        env['DJANGO_SETTINGS_MODULE'] = 'hotel_project.settings'
        
        # Использовать subprocess для вызова команды Django
        subprocess.check_call([sys.executable, "manage.py", "makemigrations"], env=env)
        print("Файлы миграций созданы успешно")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Ошибка: Не удалось создать файлы миграций: {e}")
        return False

def apply_migrations():
    """Применить миграции базы данных"""
    print("Применение миграций базы данных...")
    try:
        # Установить переменные окружения чтобы Django мог найти модуль настроек
        env = os.environ.copy()
        env['DJANGO_SETTINGS_MODULE'] = 'hotel_project.settings'
        
        subprocess.check_call([sys.executable, "manage.py", "migrate"], env=env)
        print("Миграции базы данных применены успешно")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Ошибка: Не удалось применить миграции базы данных: {e}")
        return False

def start_server():
    """Запустить сервер разработки"""
    print("Запуск сервера разработки...")
    print("Сервер будет доступен по адресу http://127.0.0.1:8000/")
    print("Нажмите Ctrl+C для остановки сервера")
    try:
        # Установить переменные окружения чтобы Django мог найти модуль настроек
        env = os.environ.copy()
        env['DJANGO_SETTINGS_MODULE'] = 'hotel_project.settings'
        
        subprocess.check_call([sys.executable, "manage.py", "runserver"], env=env)
    except subprocess.CalledProcessError as e:
        print(f"Ошибка: Не удалось запустить сервер: {e}")

def main():
    """Основная функция"""
    print("=" * 50)
    print("Скрипт быстрого запуска системы управления отелем")
    print("=" * 50)
    
    # Проверить окружение
    if not check_python():
        return
    
    # Создать виртуальную среду
    if not create_virtual_environment():
        return
    
    print("\nПожалуйста, активируйте виртуальную среду и снова запустите этот скрипт для продолжения процесса установки:")
    print("1. В Windows выполните: venv\\Scripts\\activate.bat")
    print("2. Затем снова запустите: python quick_start.py")
    
    # Если виртуальная среда уже активирована, продолжить процесс установки
    if os.path.exists('venv') and sys.prefix != sys.base_prefix:
        # Установить зависимости
        if not install_requirements():
            return
        
        # Создать и применить миграции
        if not create_migrations():
            return
        
        if not apply_migrations():
            return
        
        print("\nУстановка завершена!")
        print("Для запуска сервера выполните: python manage.py runserver")
        print("Для создания суперпользователя выполните: python manage.py createsuperuser")

if __name__ == "__main__":
    # Убедиться, что скрипт запускается в каталоге проекта
    project_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(project_dir)
    
    main()