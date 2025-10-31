from rest_framework import serializers
from .models import Booking
from rooms.models import HotelRoom
from django.utils import timezone
from django.core.exceptions import ValidationError


class BookingCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['room', 'check_in_date', 'check_out_date']

    def validate_room(self, value):
        """Проверяем, что комната существует"""
        if not HotelRoom.objects.filter(id=value.id).exists():
            raise serializers.ValidationError("Номер отеля не существует")
        return value

    def validate(self, data):
        """Валидация дат и проверка на пересечение"""
        check_in = data['check_in_date']
        check_out = data['check_out_date']
        room = data['room']
        
        # Базовая валидация дат
        if check_out <= check_in:
            raise serializers.ValidationError({
                "check_out_date": "Дата выезда должна быть позже даты заезда"
            })
        
        if check_in < timezone.now().date():
            raise serializers.ValidationError({
                "check_in_date": "Дата заезда не может быть в прошлом"
            })
        
        # Проверка на пересечение с существующими бронированиями
        overlapping_bookings = Booking.objects.filter(
            room=room
        ).filter(
            check_in_date__lt=check_out,
            check_out_date__gt=check_in
        )
        
        if overlapping_bookings.exists():
            raise serializers.ValidationError({
                "non_field_errors": ["На выбранные даты номер уже забронирован"]
            })
        
        return data


class BookingSerializer(serializers.ModelSerializer):
    room_id = serializers.IntegerField(source='room.id')
    room_description = serializers.CharField(source='room.description', read_only=True)
    
    class Meta:
        model = Booking
        fields = ['id', 'room_id', 'room_description', 'check_in_date', 'check_out_date', 'created_at']


class BookingListSerializer(serializers.ModelSerializer):
    """Сериализатор для списка бронирований номера"""
    class Meta:
        model = Booking
        fields = ['id', 'check_in_date', 'check_out_date']