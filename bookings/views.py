from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Booking
from .serializers import (
    BookingCreateSerializer, 
    BookingSerializer, 
    BookingListSerializer
)


@api_view(['POST'])
def create_booking(request):
    """Добавить бронь с проверкой на пересечение дат"""
    serializer = BookingCreateSerializer(data=request.data)
    if serializer.is_valid():
        try:
            booking = serializer.save()
            return Response(
                {'id': booking.id, 'message': 'Бронирование успешно создано'},
                status=status.HTTP_201_CREATED
            )
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
    return Response(
        {'error': serializer.errors},
        status=status.HTTP_400_BAD_REQUEST
    )


@api_view(['GET'])
def booking_detail(request, booking_id):
    """Получить детальную информацию о бронировании"""
    booking = get_object_or_404(Booking, id=booking_id)
    serializer = BookingSerializer(booking)
    return Response(serializer.data)


@api_view(['DELETE'])
def delete_booking(request, booking_id):
    """Удалить бронь"""
    booking = get_object_or_404(Booking, id=booking_id)
    booking.delete()
    
    return Response(
        {'message': f'Бронирование {booking_id} удалено'},
        status=status.HTTP_200_OK
    )


@api_view(['GET'])
def list_room_bookings(request, room_id):
    """Получить список броней номера отеля"""
    # Проверяем, что комната существует
    from rooms.models import HotelRoom
    get_object_or_404(HotelRoom, id=room_id)
    
    # Получаем все бронирования для этой комнаты, отсортированные по дате начала
    bookings = Booking.objects.filter(room_id=room_id).order_by('check_in_date')
    
    serializer = BookingListSerializer(bookings, many=True)
    return Response({'bookings': serializer.data})


@api_view(['GET'])
def check_availability(request, room_id):
    """Проверить доступность номера на определенные даты"""
    check_in = request.GET.get('check_in')
    check_out = request.GET.get('check_out')
    
    if not all([check_in, check_out]):
        return Response(
            {'error': 'Укажите check_in и check_out параметры'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        # Проверяем пересечение с существующими бронированиями
        overlapping_bookings = Booking.objects.filter(
            room_id=room_id
        ).filter(
            check_in_date__lt=check_out,
            check_out_date__gt=check_in
        )
        
        is_available = not overlapping_bookings.exists()
        
        return Response({
            'room_id': room_id,
            'check_in': check_in,
            'check_out': check_out,
            'is_available': is_available,
            'conflicting_bookings': overlapping_bookings.count() if not is_available else 0
        })
        
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_400_BAD_REQUEST
        )