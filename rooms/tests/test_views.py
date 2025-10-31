import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from rooms.models import HotelRoom
from django.shortcuts import get_object_or_404
from rest_framework.response import Response


@pytest.mark.django_db
class TestRoomAPIViews:
    def setup_method(self):
        self.client = APIClient()
        self.room_data = {
            'description': 'Люкс номер с видом на море',
            'price_per_night': '12000.00'
        }

    def test_create_room_success(self):
        """Тест успешного создания номера"""
        url = reverse('create-room')
        response = self.client.post(url, self.room_data, format='json')
        
        assert response.status_code == status.HTTP_201_CREATED
        assert 'id' in response.data
        assert HotelRoom.objects.count() == 1
        
        room = HotelRoom.objects.first()
        assert room.description == self.room_data['description']
        assert str(room.price_per_night) == self.room_data['price_per_night']

    def test_create_room_invalid_data(self):
        """Тест создания номера с невалидными данными"""
        url = reverse('create-room')
        invalid_data = {
            'description': '',  # Пустое описание
            'price_per_night': '-100.00'  # Отрицательная цена
        }
        
        response = self.client.post(url, invalid_data, format='json')
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'error' in response.data

    def test_list_rooms_success(self):
        """Тест получения списка номеров"""
        # Создаем тестовые данные
        HotelRoom.objects.create(description='Номер 1', price_per_night=3000)
        HotelRoom.objects.create(description='Номер 2', price_per_night=5000)
        
        url = reverse('list-rooms')
        response = self.client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert 'rooms' in response.data
        assert len(response.data['rooms']) == 2

    def test_list_rooms_with_sorting(self):
        """Тест сортировки списка номеров"""
        HotelRoom.objects.create(description='Дорогой номер', price_per_night=8000)
        HotelRoom.objects.create(description='Дешевый номер', price_per_night=3000)
        
        # Сортировка по цене по возрастанию
        url = f"{reverse('list-rooms')}?sort_by=price_per_night&order=asc"
        response = self.client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        rooms = response.data['rooms']
        assert float(rooms[0]['price_per_night']) == 3000.0
        assert float(rooms[1]['price_per_night']) == 8000.0

    def test_delete_room_success(self):
        """Тест успешного удаления номера"""
        room = HotelRoom.objects.create(description='Тестовый номер', price_per_night=4000)
        
        url = reverse('delete-room', args=[room.id])
        response = self.client.delete(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert HotelRoom.objects.count() == 0

    def test_delete_nonexistent_room(self):
        """Тест удаления несуществующего номера"""
        url = reverse('delete-room', args=[999])  # Несуществующий ID
        response = self.client.delete(url)
        
        assert response.status_code == status.HTTP_404_NOT_FOUND