from django.contrib import admin
from .models import HotelRoom

@admin.register(HotelRoom)
class HotelRoomAdmin(admin.ModelAdmin):
    list_display = ['id', 'description', 'price_per_night', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['description']
