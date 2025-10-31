import pytest
from datetime import date, timedelta
from rooms.models import HotelRoom
from bookings.models import Booking
from bookings.serializers import BookingCreateSerializer


@pytest.mark.django_db
class TestBookingCreateSerializer:
    def setup_method(self):
        self.room = HotelRoom.objects.create(
            description='Тестовый номер',
            price_per_night=5000.00
        )
        self.valid_data = {
            'room': self.room.id,
            'check_in_date': str(date.today() + timedelta(days=1)),
            'check_out_date': str(date.today() + timedelta(days=3))
        }

    def test_valid_serializer(self):
        """Тест валидных данных"""
        serializer = BookingCreateSerializer(data=self.valid_data)
        assert serializer.is_valid() is True

    def test_invalid_dates_check_out_before_check_in(self):
        """Тест невалидных дат (выезд раньше заезда)"""
        invalid_data = self.valid_data.copy()
        invalid_data['check_in_date'] = str(date.today() + timedelta(days=3))
        invalid_data['check_out_date'] = str(date.today() + timedelta(days=1))
        
        serializer = BookingCreateSerializer(data=invalid_data)
        assert serializer.is_valid() is False
        assert 'check_out_date' in serializer.errors

    def test_past_date_validation(self):
        """Тест даты в прошлом"""
        invalid_data = self.valid_data.copy()
        invalid_data['check_in_date'] = str(date.today() - timedelta(days=1))
        
        serializer = BookingCreateSerializer(data=invalid_data)
        assert serializer.is_valid() is False
        assert 'check_in_date' in serializer.errors

    def test_nonexistent_room_validation(self):
        """Тест несуществующего номера"""
        invalid_data = self.valid_data.copy()
        invalid_data['room'] = 999  # Несуществующий ID
        
        serializer = BookingCreateSerializer(data=invalid_data)
        assert serializer.is_valid() is False
        assert 'room' in serializer.errors