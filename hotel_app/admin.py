from django.contrib import admin
from .models import RoomType, Room, Price, Booking

@admin.register(RoomType)
class RoomTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('room_number', 'room_type', 'category', 'capacity', 'has_baby_bed', 'is_available', 'price_per_night')
    list_filter = ('room_type', 'category', 'has_baby_bed', 'is_available')
    search_fields = ('room_number',)

@admin.register(Price)
class PriceAdmin(admin.ModelAdmin):
    list_display = ('room_type', 'day_of_week', 'price')
    list_filter = ('room_type', 'day_of_week')

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('customer_name', 'customer_phone', 'room', 'check_in_date', 'check_out_date', 'status')
    list_filter = ('status', 'check_in_date', 'check_out_date')
    search_fields = ('customer_name', 'customer_phone', 'room__room_number')
    date_hierarchy = 'booking_date'