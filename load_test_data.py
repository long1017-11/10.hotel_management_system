#!/usr/bin/env python
"""
Скрипт для загрузки тестовых данных в систему управления отелем
"""

import os
import sys

def setup_django():
    """Настройка Django окружения"""
    # Добавляем путь к проекту в sys.path
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    
    # Устанавливаем переменную окружения для настроек Django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hotel_project.settings')
    
    try:
        import django
        # Настраиваем Django
        django.setup()
        return True
    except ImportError as e:
        print(f"Ошибка импорта Django: {e}")
        return False

def load_test_data():
    """Загрузка тестовых данных"""
    if not setup_django():
        print("Не удалось настроить Django окружение")
        return
    
    try:
        # Импортируем модели Django
        from hotel_app.models import RoomType, Room, Price, Booking
        from django.utils import timezone
        from datetime import datetime, timedelta
        
        print("Загрузка тестовых данных...")
        
        # Создаем типы номеров
        print("Создание типов номеров...")
        standard_type, created = RoomType.objects.get_or_create(
            name="Стандартный номер",
            defaults={"description": "Базовый уровень комфорта"}
        )
        
        comfort_type, created = RoomType.objects.get_or_create(
            name="Комфортный номер",
            defaults={"description": "Улучшенный уровень комфорта"}
        )
        
        suite_type, created = RoomType.objects.get_or_create(
            name="Люкс",
            defaults={"description": "Максимальный уровень комфорта"}
        )
        
        # Создаем номера
        print("Создание номеров...")
        rooms_data = [
            # Стандартные номера
            ("101", "single", 1, False, True, 2000),
            ("102", "single", 1, True, True, 2200),
            ("103", "double", 2, False, True, 3000),
            ("104", "double", 2, True, False, 3200),
            ("105", "triple", 3, False, True, 4000),
            
            # Комфортные номера
            ("201", "single", 1, False, True, 3000),
            ("202", "double", 2, False, True, 4500),
            ("203", "double", 2, True, True, 4800),
            ("204", "triple", 3, False, False, 5500),
            
            # Люксы
            ("301", "double", 2, True, True, 7000),
            ("302", "triple", 3, True, True, 9000),
        ]
        
        for room_data in rooms_data:
            room, created = Room.objects.get_or_create(
                room_number=room_data[0],
                defaults={
                    "room_type": standard_type if room_data[0].startswith("1") else 
                                comfort_type if room_data[0].startswith("2") else suite_type,
                    "category": room_data[1],
                    "capacity": room_data[2],
                    "has_baby_bed": room_data[3],
                    "is_available": room_data[4],
                    "price_per_night": room_data[5]
                }
            )
        
        # Создаем цены по дням недели
        print("Создание цен по дням недели...")
        price_configs = [
            (standard_type, [(0, 2000), (1, 2000), (2, 2000), (3, 2000), (4, 2200), (5, 2500), (6, 2300)]),
            (comfort_type, [(0, 3000), (1, 3000), (2, 3000), (3, 3000), (4, 3300), (5, 3800), (6, 3500)]),
            (suite_type, [(0, 7000), (1, 7000), (2, 7000), (3, 7000), (4, 8000), (5, 9000), (6, 8500)]),
        ]
        
        for room_type, prices in price_configs:
            for day, price in prices:
                Price.objects.get_or_create(
                    room_type=room_type,
                    day_of_week=day,
                    defaults={"price": price}
                )
        
        # Создаем тестовые бронирования
        print("Создание тестовых бронирований...")
        today = timezone.now().date()
        
        # Получаем комнаты заранее, чтобы избежать ошибок
        try:
            room_101 = Room.objects.get(room_number="101")
            room_201 = Room.objects.get(room_number="201")
            room_301 = Room.objects.get(room_number="301")
        except Room.DoesNotExist:
            print("Ошибка: Не удалось найти один или несколько номеров")
            return
        
        bookings_data = [
            ("Иванов Иван Иванович", "+7(999)123-45-67", room_101, 
             today + timedelta(days=1), today + timedelta(days=3), "confirmed"),
            ("Петров Петр Петрович", "+7(999)234-56-78", room_201, 
             today + timedelta(days=2), today + timedelta(days=5), "pending"),
            ("Сидоров Сидор Сидорович", "+7(999)345-67-89", room_301, 
             today - timedelta(days=1), today + timedelta(days=2), "checked_in"),
        ]
        
        for booking_data in bookings_data:
            # Вычисляем общую цену заранее
            days = (booking_data[4] - booking_data[3]).days
            total_price = booking_data[2].price_per_night * days
            
            Booking.objects.get_or_create(
                customer_name=booking_data[0],
                customer_phone=booking_data[1],
                room=booking_data[2],
                check_in_date=booking_data[3],
                check_out_date=booking_data[4],
                defaults={
                    "status": booking_data[5],
                    "total_price": total_price
                }
            )
        
        print("Тестовые данные успешно загружены!")
        
    except Exception as e:
        print(f"Ошибка при загрузке тестовых данных: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    load_test_data()