from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from rooms.models import HotelRoom
from .models import Booking
from django.utils import timezone


def bookings_list(request):
    """Список всех бронирований"""
    try:
        bookings = Booking.objects.all().select_related('room').order_by('check_in_date')
        rooms = HotelRoom.objects.all()
        
        return render(request, 'bookings/list.html', {
            'bookings': bookings,
            'rooms': rooms
        })
    except Exception as e:
        messages.error(request, f'Ошибка при загрузке бронирований: {str(e)}')
        return render(request, 'bookings/list.html', {'bookings': [], 'rooms': []})


@require_http_methods(["GET", "POST"])
def create_booking(request):
    """Создание бронирования через веб-форму с проверкой доступности"""
    rooms = HotelRoom.objects.all()
    
    if request.method == 'POST':
        try:
            room_id = request.POST.get('room')
            check_in_date = request.POST.get('check_in_date')
            check_out_date = request.POST.get('check_out_date')
            
            if not all([room_id, check_in_date, check_out_date]):
                messages.error(request, 'Заполните все поля')
                return render(request, 'bookings/create.html', {
                    'rooms': rooms,
                    'today': timezone.now().date()
                })
            
            room = get_object_or_404(HotelRoom, id=room_id)
            
            # Проверяем доступность дат
            overlapping_bookings = Booking.objects.filter(
                room=room
            ).filter(
                check_in_date__lt=check_out_date,
                check_out_date__gt=check_in_date
            )
            
            if overlapping_bookings.exists():
                messages.error(request, 'На выбранные даты номер уже забронирован')
                return render(request, 'bookings/create.html', {
                    'rooms': rooms,
                    'today': timezone.now().date(),
                    'selected_room': room_id,
                    'selected_check_in': check_in_date,
                    'selected_check_out': check_out_date
                })
            
            # Создаем бронирование
            booking = Booking.objects.create(
                room=room,
                check_in_date=check_in_date,
                check_out_date=check_out_date
            )
            messages.success(request, f'Бронирование #{booking.id} успешно создано!')
            return redirect('bookings_list')
            
        except Exception as e:
            messages.error(request, f'Ошибка при создании бронирования: {str(e)}')
    
    # GET запрос - показываем форму
    room_id = request.GET.get('room')
    initial_room = None
    if room_id:
        try:
            initial_room = HotelRoom.objects.get(id=room_id)
        except HotelRoom.DoesNotExist:
            pass
    
    return render(request, 'bookings/create.html', {
        'rooms': rooms,
        'initial_room': initial_room,
        'today': timezone.now().date()
    })


def delete_booking(request, booking_id):
    """Удаление бронирования"""
    try:
        booking = get_object_or_404(Booking, id=booking_id)
        booking.delete()
        messages.success(request, f'Бронирование #{booking_id} успешно удалено!')
    except Exception as e:
        messages.error(request, f'Ошибка при удалении: {str(e)}')
    
    return redirect('bookings_list')


def check_availability_web(request, room_id):
    """Проверка доступности номера для веб-интерфейса"""
    room = get_object_or_404(HotelRoom, id=room_id)
    check_in = request.GET.get('check_in')
    check_out = request.GET.get('check_out')
    
    if check_in and check_out:
        overlapping_bookings = Booking.objects.filter(
            room=room
        ).filter(
            check_in_date__lt=check_out,
            check_out_date__gt=check_in
        )
        is_available = not overlapping_bookings.exists()
    else:
        is_available = None
    
    return render(request, 'bookings/availability.html', {
        'room': room,
        'check_in': check_in,
        'check_out': check_out,
        'is_available': is_available,
        'today': timezone.now().date()
    })