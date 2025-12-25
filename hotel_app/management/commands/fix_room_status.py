from django.core.management.base import BaseCommand
from hotel_app.models import Room, Booking

class Command(BaseCommand):
    help = 'Проверить и исправить статус комнат после выезда гостей'

    def add_arguments(self, parser):
        parser.add_argument(
            '--fix',
            action='store_true',
            help='Автоматически исправить статус комнат',
        )

    def handle(self, *args, **options):
        self.stdout.write('Проверка статуса комнат после выезда гостей...')
        
        # Получить все комнаты
        rooms = Room.objects.all()
        fixed_count = 0
        
        for room in rooms:
            # Получить все бронирования для этой комнаты
            bookings = Booking.objects.filter(room=room)
            
            # Получить активные бронирования (не отмененные и не выселенные)
            active_bookings = bookings.exclude(status__in=['cancelled', 'checked_out'])
            
            # Если нет активных бронирований, комната должна быть доступна
            should_be_available = not active_bookings.exists()
            
            # Проверить, совпадает ли текущий статус с ожидаемым
            if room.is_available != should_be_available:
                self.stdout.write(
                    f'Комната {room.room_number}: статус не совпадает '
                    f'(текущий: {"доступна" if room.is_available else "занята"}, '
                    f'должна быть: {"доступна" if should_be_available else "занята"})'
                )
                
                # Если указан параметр исправления, автоматически исправить
                if options['fix']:
                    room.is_available = should_be_available
                    room.save()
                    fixed_count += 1
                    self.stdout.write(
                        self.style.SUCCESS(
                            f'  Исправлен статус комнаты {room.room_number}'
                        )
                    )
            else:
                self.stdout.write(
                    f'Комната {room.room_number}: статус корректный '
                    f'({"доступна" if room.is_available else "занята"})'
                )
        
        if options['fix']:
            self.stdout.write(
                self.style.SUCCESS(
                    f'Исправлено статусов {fixed_count} комнат'
                )
            )
        else:
            self.stdout.write(
                self.style.WARNING(
                    'Для автоматического исправления используйте параметр --fix'
                )
            )