import pytest
from django.core.exceptions import ValidationError
from django.utils import timezone
from rooms.models import HotelRoom


@pytest.mark.django_db
class TestHotelRoomModel:
    def test_create_hotel_room(self):
        """Тест создания номера отеля"""
        room = HotelRoom.objects.create(
            description="Комфортабельный номер с видом на море",
            price_per_night=5000.00
        )
        assert room.id is not None
        assert room.description == "Комфортабельный номер с видом на море"
        assert room.price_per_night == 5000.00
        assert room.is_active is True
        assert room.created_at is not None

    def test_room_string_representation(self):
        """Тест строкового представления номера"""
        room = HotelRoom.objects.create(
            description="Тестовый номер",
            price_per_night=3000.00
        )
        expected_string = f"Номер #{room.id} - {room.price_per_night} руб./ночь"
        assert str(room) == expected_string

    def test_room_ordering(self):
        """Тест порядка сортировки номеров"""
        room1 = HotelRoom.objects.create(description="Первый номер", price_per_night=1000)
        room2 = HotelRoom.objects.create(description="Второй номер", price_per_night=2000)
        
        rooms = HotelRoom.objects.all()
        assert rooms[0] == room2  # Последний созданный должен быть первым
        assert rooms[1] == room1