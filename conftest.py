import pytest
from django.test import RequestFactory
from rooms.models import HotelRoom
from bookings.models import Booking
from datetime import date, timedelta


@pytest.fixture
def factory():
    return RequestFactory()


@pytest.fixture
def test_room():
    """Фикстура для тестового номера отеля"""
    return HotelRoom.objects.create(
        description="Тестовый номер",
        price_per_night=5000.00
    )


@pytest.fixture
def test_booking(test_room):
    """Фикстура для тестового бронирования"""
    return Booking.objects.create(
        room=test_room,
        check_in_date=date.today() + timedelta(days=1),
        check_out_date=date.today() + timedelta(days=3)
    )