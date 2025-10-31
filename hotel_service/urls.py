from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from rooms.views_web import home, rooms_list, create_room, delete_room
from bookings.views_web import bookings_list, create_booking, delete_booking, check_availability_web

def api_home(request):
    return JsonResponse({"message": "Hotel Service API is working!", "status": "ok"})

urlpatterns = [
    # Веб-интерфейс
    path('', home, name='home'),
    path('rooms/', rooms_list, name='rooms_list'),
    path('rooms/create/', create_room, name='create_room'),
    path('rooms/<int:room_id>/delete/', delete_room, name='delete_room'),
    
    # Бронирования
    path('bookings/', bookings_list, name='bookings_list'),
    path('bookings/create/', create_booking, name='create_booking'),
    path('bookings/<int:booking_id>/delete/', delete_booking, name='delete_booking'),
    path('availability/<int:room_id>/', check_availability_web, name='check_availability_web'),
    
    # API
    path('api/', api_home, name='api_home'),
    path('api/', include('rooms.urls')),
    path('api/', include('bookings.urls')),
    path('admin/', admin.site.urls),
]