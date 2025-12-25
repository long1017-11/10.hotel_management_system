from django.db import models
from django.core.validators import MinValueValidator

class RoomType(models.Model):
    """Модель типа номера"""
    name = models.CharField('Название типа номера', max_length=50, unique=True)
    description = models.TextField('Описание', blank=True)
    
    class Meta:
        verbose_name = 'Тип номера'
        verbose_name_plural = 'Типы номеров'
    
    def __str__(self):
        return self.name

class Room(models.Model):
    """Модель номера"""
    ROOM_CATEGORY_CHOICES = [
        ('single', 'Одноместный'),
        ('double', 'Двухместный'),
        ('triple', 'Трехместный'),
    ]
    
    room_number = models.CharField('Номер комнаты', max_length=10, unique=True)
    room_type = models.ForeignKey(RoomType, on_delete=models.CASCADE, verbose_name='Тип номера')
    category = models.CharField('Категория', max_length=10, choices=ROOM_CATEGORY_CHOICES)
    capacity = models.PositiveIntegerField('Вместимость', default=1)
    # Согласно вашему требованию, все комнаты могут быть оборудованы детской кроваткой по запросу, поэтому значение по умолчанию равно True
    has_baby_bed = models.BooleanField('Детская кроватка', default=True)
    is_available = models.BooleanField('Доступен', default=True)
    price_per_night = models.DecimalField('Цена за ночь', max_digits=8, decimal_places=2, 
                                         validators=[MinValueValidator(0)])
    
    class Meta:
        verbose_name = 'Номер'
        verbose_name_plural = 'Номера'
    
    def __str__(self):
        return f"{self.room_number} - {self.room_type.name}"

class Price(models.Model):
    """Модель цены (в зависимости от дня недели)"""
    DAY_CHOICES = [
        (0, 'Понедельник'),
        (1, 'Вторник'),
        (2, 'Среда'),
        (3, 'Четверг'),
        (4, 'Пятница'),
        (5, 'Суббота'),
        (6, 'Воскресенье'),
    ]
    
    room_type = models.ForeignKey(RoomType, on_delete=models.CASCADE, verbose_name='Тип номера')
    day_of_week = models.IntegerField('День недели', choices=DAY_CHOICES)
    price = models.DecimalField('Цена', max_digits=8, decimal_places=2, 
                               validators=[MinValueValidator(0)])
    
    class Meta:
        verbose_name = 'Цена'
        verbose_name_plural = 'Цены'
        unique_together = ('room_type', 'day_of_week')
    
    def __str__(self):
        return f"{self.room_type.name} - {self.get_day_of_week_display()}: {self.price}"

class Booking(models.Model):
    """Модель бронирования"""
    STATUS_CHOICES = [
        ('pending', 'Ожидает'),
        ('confirmed', 'Подтверждено'),
        ('cancelled', 'Отменено'),
        ('checked_in', 'Проживает'),
        ('checked_out', 'Выехал'),
    ]
    
    customer_name = models.CharField('Имя клиента', max_length=100)
    customer_phone = models.CharField('Телефон клиента', max_length=20)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, verbose_name='Номер')
    check_in_date = models.DateField('Дата заезда')
    check_out_date = models.DateField('Дата выезда')
    booking_date = models.DateTimeField('Дата бронирования', auto_now_add=True)
    status = models.CharField('Статус', max_length=20, choices=STATUS_CHOICES, default='pending')
    actual_check_in_date = models.DateTimeField('Фактическая дата заезда', null=True, blank=True)
    actual_check_out_date = models.DateTimeField('Фактическая дата выезда', null=True, blank=True)
    total_price = models.DecimalField('Общая цена', max_digits=10, decimal_places=2, 
                                     validators=[MinValueValidator(0)])
    
    class Meta:
        verbose_name = 'Бронирование'
        verbose_name_plural = 'Бронирования'
    
    def __str__(self):
        return f"{self.customer_name} - {self.room.room_number}"