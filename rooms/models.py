from django.db import models

# Create your models here.

from django.utils import timezone


class HotelRoom(models.Model):
    description = models.TextField(verbose_name='Описание номера')
    price_per_night = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        verbose_name='Цена за ночь'
    )
    created_at = models.DateTimeField(
        default=timezone.now,
        verbose_name='Дата создания'
    )
    is_active = models.BooleanField(default=True, verbose_name='Активен')

    class Meta:
        db_table = 'hotel_rooms'
        verbose_name = 'Номер отеля'
        verbose_name_plural = 'Номера отелей'
        ordering = ['-created_at']

    def __str__(self):
        return f"Номер #{self.id} - {self.price_per_night} руб./ночь"


class RoomImage(models.Model):
    room = models.ForeignKey(
        HotelRoom, 
        on_delete=models.CASCADE, 
        related_name='images'
    )
    image = models.ImageField(upload_to='room_images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'room_images'