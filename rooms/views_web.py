from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from .models import HotelRoom
import requests


def home(request):
    """Главная страница"""
    return render(request, 'index.html')


def rooms_list(request):
    """Список номеров"""
    try:
        # Используем API для получения данных
        response = requests.get('http://localhost:8000/api/rooms/list/')
        if response.status_code == 200:
            rooms = response.json().get('rooms', [])
        else:
            rooms = []
            messages.error(request, 'Ошибка при загрузке номеров')
    except:
        rooms = HotelRoom.objects.all().values()
    
    return render(request, 'rooms/list.html', {'rooms': rooms})


@require_http_methods(["GET", "POST"])
def create_room(request):
    """Создание номера через веб-форму"""
    if request.method == 'POST':
        try:
            # Используем API для создания
            response = requests.post(
                'http://localhost:8000/api/rooms/',
                json={
                    'description': request.POST.get('description'),
                    'price_per_night': request.POST.get('price_per_night')
                }
            )
            
            if response.status_code == 201:
                messages.success(request, 'Номер успешно создан!')
                return redirect('rooms_list')
            else:
                messages.error(request, f'Ошибка: {response.json().get("error", "Неизвестная ошибка")}')
        except Exception as e:
            messages.error(request, f'Ошибка соединения: {str(e)}')
    
    return render(request, 'rooms/create.html')


def delete_room(request, room_id):
    """Удаление номера"""
    try:
        response = requests.delete(f'http://localhost:8000/api/rooms/{room_id}/delete/')
        if response.status_code == 200:
            messages.success(request, 'Номер успешно удален!')
        else:
            messages.error(request, 'Ошибка при удалении номера')
    except Exception as e:
        messages.error(request, f'Ошибка соединения: {str(e)}')
    
    return redirect('rooms_list')