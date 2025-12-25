from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('rooms/', views.room_management, name='room_management'),
    path('room-status/', views.room_status, name='room_status'),
    path('bookings/', views.booking_list, name='booking_list'),
    path('bookings/cancel/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),
    path('check-in-out/', views.check_in_out, name='check_in_out'),
    path('check-in-guest/', views.check_in_guest, name='check_in_guest'),
    path('pricing/', views.pricing_info, name='pricing_info'),
    path('test/', views.test_view, name='test_view'),
    path('test-static/', views.test_static, name='test_static'),
]