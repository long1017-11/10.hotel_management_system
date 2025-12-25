from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.utils import timezone
from django.http import HttpResponse
from .models import Room, RoomType, Booking, Price
from .forms import CheckInForm
from datetime import date

def update_room_availability(room):
    """Обновить статус доступности комнаты"""
    try:
        # Проверить, есть ли активные бронирования (не отмененные и не выселенные) для этой комнаты
        active_bookings = Booking.objects.filter(
            room=room
        ).exclude(
            status__in=['cancelled', 'checked_out']
        )
        
        # 如果没有 активных бронирований, номер должен быть доступен
        should_be_available = not active_bookings.exists()
        
        # 打印调试信息
        print(f"DEBUG: 房间 {room.room_number} 的状态检查:")
        print(f"DEBUG: 活跃预订数量: {active_bookings.count()}")
        print(f"DEBUG: 房间当前状态: {'可用' if room.is_available else '占用'}")
        print(f"DEBUG: 房间应该状态: {'可用' if should_be_available else '占用'}")
        
        # Обновить статус комнаты только если он изменился
        if room.is_available != should_be_available:
            room.is_available = should_be_available
            room.save()
            print(f"Комната {room.room_number} теперь {'доступна' if should_be_available else 'занята'}")
            # 添加成功更新的调试信息
            print(f"DEBUG: 房间 {room.room_number} 状态已更新")
        else:
            print(f"DEBUG: 房间 {room.room_number} 状态无需更新")
    except Exception as e:
        print(f"Ошибка при обновлении статуса комнаты {room.room_number}: {e}")

def get_room_status_info():
    """Получить комнаты статус информацию"""
    try:
        # Получить все комнаты их статус
        rooms = Room.objects.all().order_by('room_number')
        room_status_info = []
        
        for room in rooms:
            # Получить все бронирования для этой комнаты
            bookings = Booking.objects.filter(room=room)
            # Получить бронирования которые не отменены и не выселены
            active_bookings = bookings.exclude(status__in=['cancelled', 'checked_out'])
            
            room_status_info.append({
                'room': room,
                'is_occupied': not room.is_available,
                'active_bookings': active_bookings
            })
        
        return room_status_info
    except Exception as e:
        print(f"Ошибка при получении информации о статусе комнат: {e}")
        return []

def room_management(request):
    """Room management view"""
    try:
        # Get all room types and their available counts
        room_types = RoomType.objects.all()
        room_info = []
        
        for room_type in room_types:
            total_rooms = Room.objects.filter(room_type=room_type).count()
            available_rooms = Room.objects.filter(room_type=room_type, is_available=True).count()
            occupied_rooms = total_rooms - available_rooms
            room_info.append({
                'type': room_type,
                'total': total_rooms,
                'available': available_rooms,
                'occupied': occupied_rooms
            })
        
        context = {
            'room_info': room_info
        }
        return render(request, 'hotel_app/room_management.html', context)
    except Exception as e:
        messages.error(request, f'Ошибка при загрузке данных: {e}')
        return render(request, 'hotel_app/room_management.html', {'room_info': []})

def booking_list(request):
    """Booking list view"""
    try:
        bookings = Booking.objects.all().order_by('-booking_date')
        context = {
            'bookings': bookings
        }
        return render(request, 'hotel_app/booking_list.html', context)
    except Exception as e:
        messages.error(request, f'Ошибка при загрузке бронирований: {e}')
        return render(request, 'hotel_app/booking_list.html', {'bookings': []})

def cancel_booking(request, booking_id):
    """Cancel booking view"""
    try:
        booking = get_object_or_404(Booking, id=booking_id)
        if request.method == 'POST':
            old_status = booking.status
            booking.status = 'cancelled'
            booking.save()
            
            # Обновить комнату как доступную
            try:
                update_room_availability(booking.room)
            except Exception as e:
                messages.error(request, f'Ошибка при обновлении статуса комнаты: {e}')
            
            messages.success(request, 'Бронирование успешно отменено')
            return redirect('booking_list')
        
        context = {
            'booking': booking
        }
        return render(request, 'hotel_app/cancel_booking.html', context)
    except Exception as e:
        messages.error(request, f'Ошибка при отмене бронирования: {e}')
        return redirect('booking_list')

def check_in_out(request):
    """Check-in/Check-out view"""
    try:
        if request.method == 'POST':
            booking_id = request.POST.get('booking_id')
            action = request.POST.get('action')  # 'check_in' or 'check_out'
            redirect_to = request.POST.get('redirect_to')  # Цель перенаправления
            
            booking = get_object_or_404(Booking, id=booking_id)
            if action == 'check_in':
                booking.status = 'checked_in'
                booking.actual_check_in_date = timezone.now()
                messages.success(request, 'Регистрация заезда прошла успешно')
            elif action == 'check_out':
                booking.status = 'checked_out'
                booking.actual_check_out_date = timezone.now()
                
                # Обновить комнату как доступную
                try:
                    update_room_availability(booking.room)
                except Exception as e:
                    messages.error(request, f'Ошибка при обновлении статуса комнаты: {e}')
                
                messages.success(request, 'Регистрация выезда прошла успешно')
            booking.save()
            # Определить цель перенаправления на основе параметра redirect_to
            if action == 'check_out':
                if redirect_to == 'room_status':
                    return redirect('room_status')
                elif redirect_to == 'current_page':
                    # Перенаправить на текущую страницу после выезда с параметром успеха
                    return redirect('{}?checkout_success=1'.format(request.path))
                else:
                    return redirect('check_in_out')
            return redirect('check_in_out')
        
        # Получить все записи о заезде и выезде
        check_in_bookings = Booking.objects.filter(status='checked_in')
        check_out_bookings = Booking.objects.filter(status='checked_out')
        
        context = {
            'check_in_bookings': check_in_bookings,
            'check_out_bookings': check_out_bookings
        }
        return render(request, 'hotel_app/check_in_out.html', context)
    except Exception as e:
        messages.error(request, f'Ошибка при обработке заезда/выезда: {e}')
        return render(request, 'hotel_app/check_in_out.html', {
            'check_in_bookings': [],
            'check_out_bookings': []
        })

def pricing_info(request):
    """Pricing information view"""
    try:
        prices = Price.objects.select_related('room_type').all()
        
        # Организовать информацию о ценах по типам номеров
        price_dict = {}
        for price in prices:
            if price.room_type.name not in price_dict:
                price_dict[price.room_type.name] = {}
            price_dict[price.room_type.name][price.get_day_of_week_display()] = float(price.price)
        
        context = {
            'price_dict': price_dict
        }
        return render(request, 'hotel_app/pricing_info.html', context)
    except Exception as e:
        messages.error(request, f'Ошибка при загрузке цен: {e}')
        return render(request, 'hotel_app/pricing_info.html', {'price_dict': {}})

def test_view(request):
    """Test view"""
    return HttpResponse(b"Django \xd1\x80\xd0\xb0\xd0\xb1\xd0\xbe\xd1\x82\xd0\xb0\xd0\xb5\xd1\x82 \xd0\xba\xd0\xbe\xd1\x80\xd1\x80\xd0\xb5\xd0\xba\xd1\x82\xd0\xbd\xd0\xbe! \xd0\xa1\xd0\xb8\xd1\x81\xd1\x82\xd0\xb5\xd0\xbc\xd0\xb0 \xd1\x83\xd0\xbf\xd1\x80\xd0\xb0\xd0\xb2\xd0\xbb\xd0\xb5\xd0\xbd\xd0\xb8\xd1\x8f \xd0\xbe\xd1\x82\xd0\xb5\xd0\xbb\xd0\xb5\xd0\xbc \xd0\xb3\xd0\xbe\xd1\x82\xd0\xbe\xd0\xb2\xd0\xb0 \xd0\xba \xd0\xb8\xd1\x81\xd0\xbf\xd0\xbe\xd0\xbb\xd1\x8c\xd0\xb7\xd0\xbe\xd0\xb2\xd0\xb0\xd0\xbd\xd0\xb8\xd1\x8e.")

def test_static(request):
    """Test static files view"""
    return render(request, 'hotel_app/test_static.html')

def check_in_guest(request):
    """View for checking in guests"""
    if request.method == 'POST':
        # Проверка, является ли запрос расчетом цены
        if 'calculate_price' in request.POST:
            form = CheckInForm(request.POST)
            if form.is_valid():
                # Получить данные формы
                customer_name = form.cleaned_data['customer_name']
                customer_phone = form.cleaned_data['customer_phone']
                customer_email = form.cleaned_data['customer_email']
                room_type = form.cleaned_data['room_type']
                has_baby_bed = form.cleaned_data['has_baby_bed']
                check_in_date = form.cleaned_data['check_in_date']
                check_out_date = form.cleaned_data['check_out_date']
                
                # Валидация дат
                if check_out_date <= check_in_date:
                    messages.error(request, 'Дата выезда должна быть позже даты заезда')
                    return render(request, 'hotel_app/check_in_guest.html', {'form': form})
                
                # Найти доступную комнату
                try:
                    # Сначала найти полностью соответствующую комнату
                    available_room = Room.objects.filter(
                        room_type=room_type,
                        has_baby_bed=has_baby_bed,
                        is_available=True
                    ).first()
                    
                    # Если нет полностью соответствующей комнаты, найти комнату того же типа
                    if not available_room:
                        available_room = Room.objects.filter(
                            room_type=room_type,
                            is_available=True
                        ).first()
                    
                    if available_room:
                        # Расчет общей стоимости
                        total_price = calculate_total_price(available_room, check_in_date, check_out_date)
                        
                        # Сохранить данные в session для последующего использования
                        request.session['check_in_data'] = {
                            'customer_name': customer_name,
                            'customer_phone': customer_phone,
                            'customer_email': customer_email,
                            'room_type_id': room_type.id,
                            'has_baby_bed': has_baby_bed,
                            'check_in_date': check_in_date.isoformat(),
                            'check_out_date': check_out_date.isoformat(),
                            'room_id': available_room.id,
                            'total_price': total_price
                        }
                        
                        # Передать данные в шаблон для отображения цены
                        context = {
                            'form': form,
                            'calculated': True,
                            'total_price': total_price,
                            'available_room': available_room,
                            'check_in_date': check_in_date,
                            'check_out_date': check_out_date,
                            'customer_name': customer_name,
                            'customer_phone': customer_phone,
                            'customer_email': customer_email
                        }
                        return render(request, 'hotel_app/check_in_guest.html', context)
                    else:
                        messages.error(request, 'Нет доступных номеров выбранного типа')
                        return render(request, 'hotel_app/check_in_guest.html', {'form': form})
                except Exception as e:
                    messages.error(request, f'Ошибка при расчете стоимости: {e}')
                    return render(request, 'hotel_app/check_in_guest.html', {'form': form})
            else:
                return render(request, 'hotel_app/check_in_guest.html', {'form': form})
        
        # Проверка, является ли запрос подтверждением заезда
        elif 'confirm_check_in' in request.POST:
            # Получить данные из session
            check_in_data = request.session.get('check_in_data')
            if not check_in_data:
                messages.error(request, 'Данные о регистрации заезда утеряны. Пожалуйста, начните заново.')
                form = CheckInForm()
                form.fields['room_type'].queryset = RoomType.objects.all()
                return render(request, 'hotel_app/check_in_guest.html', {'form': form})
            
            try:
                # Получить объект комнаты
                room = Room.objects.get(id=check_in_data['room_id'])
                
                # Создать запись бронирования
                booking = Booking.objects.create(
                    customer_name=check_in_data['customer_name'],
                    customer_phone=check_in_data['customer_phone'],
                    room=room,
                    check_in_date=date.fromisoformat(check_in_data['check_in_date']),
                    check_out_date=date.fromisoformat(check_in_data['check_out_date']),
                    status='checked_in',
                    actual_check_in_date=timezone.now(),
                    total_price=check_in_data['total_price']
                )
                
                # Обновить статус комнаты на занятую
                try:
                    update_room_availability(room)
                except Exception as e:
                    messages.error(request, f'Ошибка при обновлении статуса комнаты: {e}')
                
                # Очистить данные в session
                del request.session['check_in_data']
                
                messages.success(request, f'Гость {check_in_data["customer_name"]} успешно зарегистрирован в номере {room.room_number}. Общая стоимость: {check_in_data["total_price"]} руб.')
                return redirect('check_in_guest')
            except Exception as e:
                messages.error(request, f'Ошибка при регистрации заезда: {e}')
                form = CheckInForm()
                form.fields['room_type'].queryset = RoomType.objects.all()
                return render(request, 'hotel_app/check_in_guest.html', {'form': form})
    else:
        form = CheckInForm()
        # Manually set the queryset to ensure data is loaded
        form.fields['room_type'].queryset = RoomType.objects.all()
    
    return render(request, 'hotel_app/check_in_guest.html', {'form': form})

def calculate_total_price(room, check_in_date, check_out_date):
    """Расчет общей стоимости"""
    try:
        # Расчет количества ночей
        days = (check_out_date - check_in_date).days
        
        if days <= 0:
            return 0
            
        total_price = 0
        current_date = check_in_date
        
        # Рассчитать цену за каждый день
        while current_date < check_out_date:
            # Получить день недели (0=Понедельник, 6=Воскресенье)
            day_of_week = current_date.weekday()
            
            # Получить цену для типа номера и дня недели
            try:
                price = Price.objects.get(room_type=room.room_type, day_of_week=day_of_week)
                total_price += float(price.price)
            except Price.DoesNotExist:
                # Если цена не установлена, использовать цену по умолчанию для номера
                total_price += float(room.price_per_night)
            
            # Перейти к следующему дню
            current_date = date.fromordinal(current_date.toordinal() + 1)
        
        return total_price
    except Exception as e:
        print(f"Ошибка при расчете стоимости: {e}")
        return 0

def room_status(request):
    """Room status view"""
    try:
        # Получить информацию о статусе номеров
        room_status_info = get_room_status_info()
        context = {
            'room_status_info': room_status_info
        }
        return render(request, 'hotel_app/room_status.html', context)
    except Exception as e:
        messages.error(request, f'Ошибка при загрузке данных о номерах: {e}')
        return render(request, 'hotel_app/room_status.html', {'room_status_info': []})

def home(request):
    """Home page view"""
    return render(request, 'hotel_app/home.html')