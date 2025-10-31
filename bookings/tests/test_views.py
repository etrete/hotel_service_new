import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from datetime import date, timedelta
from rooms.models import HotelRoom
from bookings.models import Booking


@pytest.mark.django_db
class TestBookingAPIViews:
    def setup_method(self):
        self.client = APIClient()
        self.room = HotelRoom.objects.create(
            description='Тестовый номер',
            price_per_night=5000.00
        )
        # Будущие даты для тестов
        self.future_date_1 = date.today() + timedelta(days=10)
        self.future_date_2 = date.today() + timedelta(days=15)
        self.future_date_3 = date.today() + timedelta(days=20)
        self.future_date_4 = date.today() + timedelta(days=25)
        
        self.booking_data = {
            'room': self.room.id,
            'check_in_date': str(self.future_date_1),
            'check_out_date': str(self.future_date_2)
        }

    def test_create_booking_success(self):
        """Тест успешного создания бронирования"""
        url = reverse('create-booking')
        response = self.client.post(url, self.booking_data, format='json')
        
        assert response.status_code == status.HTTP_201_CREATED
        assert 'id' in response.data
        assert Booking.objects.count() == 1
        
        booking = Booking.objects.first()
        assert booking.room == self.room
        assert booking.check_in_date == self.future_date_1

    def test_create_booking_overlap(self):
        """Тест создания бронирования с пересекающимися датами"""
        # Первое бронирование
        Booking.objects.create(
            room=self.room,
            check_in_date=self.future_date_1,
            check_out_date=self.future_date_2
        )
        
        # Второе бронирование с пересечением
        overlapping_data = {
            'room': self.room.id,
            'check_in_date': str(self.future_date_1 + timedelta(days=2)),  # Пересекается
            'check_out_date': str(self.future_date_3)
        }
        
        url = reverse('create-booking')
        response = self.client.post(url, overlapping_data, format='json')
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'error' in response.data
        assert 'уже забронирован' in str(response.data['error']).lower()

    def test_check_availability_available(self):
        """Тест проверки доступности номера (доступен)"""
        url = reverse('check-availability', args=[self.room.id])
        params = {
            'check_in': str(self.future_date_1),
            'check_out': str(self.future_date_2)
        }
        
        response = self.client.get(url, params)
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['is_available'] is True
        assert response.data['conflicting_bookings'] == 0

    def test_check_availability_not_available(self):
        """Тест проверки доступности номера (не доступен)"""
        # Создаем существующее бронирование
        Booking.objects.create(
            room=self.room,
            check_in_date=self.future_date_1,
            check_out_date=self.future_date_2
        )
        
        url = reverse('check-availability', args=[self.room.id])
        params = {
            'check_in': str(self.future_date_1 + timedelta(days=1)),  # Пересекается
            'check_out': str(self.future_date_1 + timedelta(days=3))
        }
        
        response = self.client.get(url, params)
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['is_available'] is False
        assert response.data['conflicting_bookings'] == 1

    def test_list_room_bookings(self):
        """Тест получения списка бронирований номера"""
        # Создаем бронирования
        Booking.objects.create(
            room=self.room,
            check_in_date=self.future_date_1,
            check_out_date=self.future_date_2
        )
        Booking.objects.create(
            room=self.room,
            check_in_date=self.future_date_3,
            check_out_date=self.future_date_4
        )
        
        url = reverse('list-room-bookings', args=[self.room.id])
        response = self.client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert 'bookings' in response.data
        assert len(response.data['bookings']) == 2

    def test_delete_booking(self):
        """Тест удаления бронирования"""
        booking = Booking.objects.create(
            room=self.room,
            check_in_date=self.future_date_1,
            check_out_date=self.future_date_2
        )
        
        url = reverse('delete-booking', args=[booking.id])
        response = self.client.delete(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert Booking.objects.count() == 0