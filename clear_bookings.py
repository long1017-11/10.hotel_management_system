#!/usr/bin/env python
import os
import django

# Настройка среды Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hotel_project.settings')
django.setup()

from hotel_app.models import Room, Booking

def clear_all_bookings():
    """Очистить всю информацию о бронировании и сбросить статус номеров"""
    print("Начало очистки информации о всех гостях...")
    
    # Получить все записи о бронировании
    bookings = Booking.objects.all()
    total_bookings = bookings.count()
    
    if total_bookings > 0:
        # Удалить все записи о бронировании
        bookings.delete()
        print(f"Удалено {total_bookings} записей о бронировании")
    else:
        print("Нет записей о бронировании для удаления")
    
    # Получить все номера
    rooms = Room.objects.all()
    updated_rooms = 0
    
    # Установить все номера в свободное состояние
    for room in rooms:
        if not room.is_available:
            room.is_available = True
            room.save()
            updated_rooms += 1
    
    print(f"Установлено свободное состояние для {updated_rooms} номеров")
    print("Вся информация о гостях очищена, статус номеров сброшен!")

if __name__ == "__main__":
    clear_all_bookings()