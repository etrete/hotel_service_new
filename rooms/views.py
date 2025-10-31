
# Create your views here.

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db import transaction
from django.shortcuts import get_object_or_404
from .models import HotelRoom
from .serializers import (
    HotelRoomSerializer, 
    HotelRoomCreateSerializer,
    HotelRoomListSerializer
)


@api_view(['POST'])
def create_room(request):
    """Добавить номер отеля"""
    serializer = HotelRoomCreateSerializer(data=request.data)
    if serializer.is_valid():
        room = serializer.save()
        return Response(
            {'id': room.id, 'message': 'Номер успешно создан'},
            status=status.HTTP_201_CREATED
        )
    return Response(
        {'error': serializer.errors},
        status=status.HTTP_400_BAD_REQUEST
    )


@api_view(['DELETE'])
def delete_room(request, room_id):
    """Удалить номер отеля и все его брони"""
    try:
        with transaction.atomic():
            # Пробуем найти комнату
            room = HotelRoom.objects.get(id=room_id)
            
            # Удаляем все связанные бронирования
            room.bookings.all().delete()
            
            # Удаляем сам номер
            room.delete()
            
            return Response(
                {'message': f'Номер {room_id} и все его брони удалены'},
                status=status.HTTP_200_OK
            )
    except HotelRoom.DoesNotExist:
        return Response(
            {'error': f'Номер с ID {room_id} не найден'},
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return Response(
            {'error': f'Ошибка при удалении: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
def list_rooms(request):
    """Получить список номеров отеля с сортировкой"""
    rooms = HotelRoom.objects.filter(is_active=True)
    
    # Параметры сортировки
    sort_by = request.GET.get('sort_by', 'created_at')
    order = request.GET.get('order', 'desc')
    
    # Валидация параметров сортировки
    valid_sort_fields = ['price_per_night', 'created_at']
    if sort_by not in valid_sort_fields:
        return Response(
            {'error': f'Недопустимое поле для сортировки. Допустимые: {valid_sort_fields}'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Определение направления сортировки
    if order == 'asc':
        sort_field = sort_by
    else:
        sort_field = f'-{sort_by}'
    
    # Применение сортировки
    rooms = rooms.order_by(sort_field)
    
    serializer = HotelRoomListSerializer(rooms, many=True)
    return Response({'rooms': serializer.data})


@api_view(['GET'])
def room_detail(request, room_id):
    """Получить детальную информацию о номере"""
    room = get_object_or_404(HotelRoom, id=room_id, is_active=True)
    serializer = HotelRoomSerializer(room)
    return Response(serializer.data)