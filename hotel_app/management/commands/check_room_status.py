from django.core.management.base import BaseCommand
from hotel_app.models import Room, Booking

class Command(BaseCommand):
    help = 'Проверить и исправить проблемы несоответствия статуса номеров'

    def add_arguments(self, parser):
        parser.add_argument(
            '--fix',
            action='store_true',
            help='Автоматически исправить проблемы несоответствия статуса номеров',
        )

    def handle(self, *args, **options):
        self.stdout.write('Начало проверки статуса номеров...')
        
        # Получить все номера
        rooms = Room.objects.all()
        inconsistent_count = 0
        fixed_count = 0
        
        for room in rooms:
            # Получить все бронирования для этого номера
            bookings = Booking.objects.filter(room=room)
            
            # Проверить наличие активных (не отмененных и не выехавших) бронирований
            active_bookings = bookings.exclude(status__in=['cancelled', 'checked_out'])
            
            # Определить статус номера на основе активных бронирований
            should_be_available = not active_bookings.exists()
            
            # Проверить соответствие статуса номера
            if room.is_available != should_be_available:
                inconsistent_count += 1
                status_text = "Свободен" if room.is_available else "Занят"
                should_be_text = "Свободен" if should_be_available else "Занят"
                
                self.stdout.write(
                    f'Номер {room.room_number}: несоответствие статуса '
                    f'(текущий: {status_text}, должен быть: {should_be_text})'
                )
                
                # Если указан параметр исправления, автоматически исправить
                if options['fix']:
                    room.is_available = should_be_available
                    room.save()
                    fixed_count += 1
                    self.stdout.write(
                        self.style.SUCCESS(
                            f'  Исправлен статус номера {room.room_number}'
                        )
                    )
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Проверка завершена! Найдено {inconsistent_count} несоответствий статуса номеров'
            )
        )
        
        if options['fix']:
            self.stdout.write(
                self.style.SUCCESS(
                    f'Исправлено статусов {fixed_count} номеров'
                )
            )