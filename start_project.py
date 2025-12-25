#!/usr/bin/env python
"""
Скрипт запуска системы управления отелем в один клик
Автоматически обрабатывает создание виртуальной среды, установку зависимостей, миграцию базы данных и все другие шаги
"""

import os
import sys
import subprocess
import venv

def run_command(command, env=None):
    """Выполнить команду и вернуть результат"""
    try:
        result = subprocess.run(command, shell=True, check=True, 
                              capture_output=True, text=True, env=env)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Ошибка выполнения команды: {command}")
        print(f"Сообщение об ошибке: {e.stderr}")
        return None

def main():
    print("=" * 60)
    print("Скрипт запуска системы управления отелем в один клик")
    print("=" * 60)
    
    # Проверить, находимся ли мы в каталоге проекта
    if not os.path.exists('manage.py'):
        print("Ошибка: Файл manage.py не найден. Пожалуйста, запустите этот скрипт в корневом каталоге проекта.")
        return
    
    # Установить каталог проекта
    project_dir = os.getcwd()
    print(f"Каталог проекта: {project_dir}")
    
    # Создать виртуальную среду
    print("\n1. Создание виртуальной среды...")
    if not os.path.exists('venv'):
        try:
            venv.create('venv', with_pip=True)
            print("   Виртуальная среда создана успешно")
        except Exception as e:
            print(f"   Ошибка: Не удалось создать виртуальную среду: {e}")
            return
    else:
        print("   Виртуальная среда уже существует")
    
    # Активировать виртуальную среду и установить переменные окружения
    print("\n2. Настройка окружения...")
    env = os.environ.copy()
    
    # Установить путь Python
    if os.name == 'nt':  # Windows
        python_exe = os.path.join('venv', 'Scripts', 'python.exe')
        pip_exe = os.path.join('venv', 'Scripts', 'pip.exe')
    else:  # Unix/Linux/Mac
        python_exe = os.path.join('venv', 'bin', 'python')
        pip_exe = os.path.join('venv', 'bin', 'pip')
    
    # Убедиться, что исполняемый файл Python существует
    if not os.path.exists(python_exe):
        print(f"Ошибка: Исполняемый файл Python не найден: {python_exe}")
        return
    
    # Установить модуль настроек Django
    env['DJANGO_SETTINGS_MODULE'] = 'hotel_project.settings'
    
    # Обновить pip
    print("\n3. Обновление pip...")
    result = run_command(f'"{python_exe}" -m pip install --upgrade pip', env=env)
    if result is None:
        return
    print("   pip успешно обновлен")
    
    # Установить зависимости
    print("\n4. Установка зависимостей проекта...")
    result = run_command(f'"{python_exe}" -m pip install -r requirements.txt', env=env)
    if result is None:
        return
    print("   Зависимости установлены успешно")
    
    # Создать миграции базы данных
    print("\n5. Создание миграций базы данных...")
    result = run_command(f'"{python_exe}" manage.py makemigrations', env=env)
    if result is None:
        return
    print("   Файлы миграций базы данных созданы успешно")
    
    # Применить миграции базы данных
    print("\n6. Применение миграций базы данных...")
    result = run_command(f'"{python_exe}" manage.py migrate', env=env)
    if result is None:
        return
    print("   Миграции базы данных применены успешно")
    
    print("\n" + "=" * 60)
    print("Установка завершена!")
    print("=" * 60)
    print("Теперь вы можете выполнить следующие действия:")
    print(f"1. Запустить сервер разработки: {python_exe} manage.py runserver")
    print(f"2. Создать суперпользователя: {python_exe} manage.py createsuperuser")
    print("\nПодсказки:")
    print("- Сервер будет доступен по адресу http://127.0.0.1:8000/")
    print("- Панель администратора по адресу http://127.0.0.1:8000/admin/")
    print("- Используйте Ctrl+C для остановки сервера")

if __name__ == "__main__":
    main()