from django.contrib import admin
from .models import Booking

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['id', 'room', 'check_in_date', 'check_out_date', 'created_at']
    list_filter = ['check_in_date', 'check_out_date']
    search_fields = ['room__description']
    date_hierarchy = 'created_at'