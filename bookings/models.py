from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from rooms.models import HotelRoom


class Booking(models.Model):
    room = models.ForeignKey(
        HotelRoom, 
        on_delete=models.CASCADE,
        related_name='bookings',
        verbose_name='Номер отеля'
    )
    check_in_date = models.DateField(verbose_name='Дата заезда')
    check_out_date = models.DateField(verbose_name='Дата выезда')
    created_at = models.DateTimeField(default=timezone.now, verbose_name='Дата создания')

    class Meta:
        db_table = 'bookings'
        verbose_name = 'Бронирование'
        verbose_name_plural = 'Бронирования'
        ordering = ['check_in_date']
        constraints = [
            models.UniqueConstraint(
                fields=['room', 'check_in_date', 'check_out_date'],
                name='unique_booking_per_room_dates'
            )
        ]

    def clean(self):
        """Валидация дат и проверка на пересечение с существующими бронированиями"""
        # Базовая валидация дат
        if self.check_out_date <= self.check_in_date:
            raise ValidationError('Дата выезда должна быть позже даты заезда')
        
        if self.check_in_date < timezone.now().date():
            raise ValidationError('Дата заезда не может быть в прошлом')
        
        # Проверка на пересечение с существующими бронированиями
        if self._check_booking_overlap():
            raise ValidationError('На выбранные даты номер уже забронирован')

    def _check_booking_overlap(self):
        """Проверяет пересечение с существующими бронированиями"""
        overlapping_bookings = Booking.objects.filter(
            room=self.room
        ).exclude(
            pk=self.pk  # Исключаем текущее бронирование при обновлении
        ).filter(
            # Проверяем пересечение дат
            check_in_date__lt=self.check_out_date,
            check_out_date__gt=self.check_in_date
        )
        
        return overlapping_bookings.exists()

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Бронирование #{self.id} - комната #{self.room.id} ({self.check_in_date} - {self.check_out_date})"