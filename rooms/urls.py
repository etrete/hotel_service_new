from django.urls import path
from . import views

urlpatterns = [
    path('rooms/', views.create_room, name='create-room'),
    path('rooms/list/', views.list_rooms, name='list-rooms'),
    path('rooms/<int:room_id>/', views.room_detail, name='room-detail'),
    path('rooms/<int:room_id>/delete/', views.delete_room, name='delete-room'),
]