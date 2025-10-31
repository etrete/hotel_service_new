from django.urls import path
from . import views
from .views_web import check_availability_web

urlpatterns = [
    # API endpoints
    path('bookings/', views.create_booking, name='create-booking'),
    path('bookings/<int:booking_id>/', views.booking_detail, name='booking-detail'),
    path('bookings/<int:booking_id>/delete/', views.delete_booking, name='delete-booking'),
    path('rooms/<int:room_id>/bookings/', views.list_room_bookings, name='list-room-bookings'),
    path('availability/<int:room_id>/', views.check_availability, name='check-availability'),
    
    # Web endpoints
    path('web/availability/<int:room_id>/', check_availability_web, name='check-availability-web'),
]