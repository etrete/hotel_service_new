import pytest
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import date, timedelta
from rooms.models import HotelRoom
from bookings.models import Booking


@pytest.mark.django_db
class TestBookingModel:
    def setup_method(self):
        """Создаем тестовый номер отеля"""
        self.room = HotelRoom.objects.create(
            description="Тестовый номер",
            price_per_night=5000.00
        )
        # Будущие даты для тестов
        self.future_date_1 = date.today() + timedelta(days=10)
        self.future_date_2 = date.today() + timedelta(days=15)
        self.future_date_3 = date.today() + timedelta(days=20)
        self.future_date_4 = date.today() + timedelta(days=25)

    def test_create_booking(self):
        """Тест создания бронирования"""
        check_in = date.today() + timedelta(days=1)
        check_out = date.today() + timedelta(days=3)
        
        booking = Booking.objects.create(
            room=self.room,
            check_in_date=check_in,
            check_out_date=check_out
        )
        
        assert booking.id is not None
        assert booking.room == self.room
        assert booking.check_in_date == check_in
        assert booking.check_out_date == check_out

    def test_booking_validation_check_out_before_check_in(self):
        """Тест валидации: дата выезда раньше даты заезда"""
        check_in = date.today() + timedelta(days=3)
        check_out = date.today() + timedelta(days=1)
        
        booking = Booking(
            room=self.room,
            check_in_date=check_in,
            check_out_date=check_out
        )
        
        with pytest.raises(ValidationError) as exc_info:
            booking.full_clean()
        
        assert 'Дата выезда должна быть позже даты заезда' in str(exc_info.value)

    def test_booking_validation_past_date(self):
        """Тест валидации: дата заезда в прошлом"""
        check_in = date.today() - timedelta(days=1)
        check_out = date.today() + timedelta(days=2)
        
        booking = Booking(
            room=self.room,
            check_in_date=check_in,
            check_out_date=check_out
        )
        
        with pytest.raises(ValidationError) as exc_info:
            booking.full_clean()
        
        assert 'Дата заезда не может быть в прошлом' in str(exc_info.value)

    def test_booking_overlap_detection(self):
        """Тест обнаружения пересечения бронирований"""
        # Первое бронирование
        Booking.objects.create(
            room=self.room,
            check_in_date=self.future_date_1,  # 10 дней от сегодня
            check_out_date=self.future_date_2   # 15 дней от сегодня
        )
        
        # Второе бронирование с пересечением
        booking2 = Booking(
            room=self.room,
            check_in_date=self.future_date_1 + timedelta(days=2),  # 12 дней - пересекается
            check_out_date=self.future_date_3                      # 20 дней
        )
        
        with pytest.raises(ValidationError) as exc_info:
            booking2.full_clean()
        
        assert 'На выбранные даты номер уже забронирован' in str(exc_info.value)

    def test_booking_no_overlap(self):
        """Тест что непересекающиеся бронирования создаются нормально"""
        # Первое бронирование
        Booking.objects.create(
            room=self.room,
            check_in_date=self.future_date_1,  # 10 дней от сегодня
            check_out_date=self.future_date_2   # 15 дней от сегодня
        )
        
        # Второе бронирование без пересечения
        booking2 = Booking(
            room=self.room,
            check_in_date=self.future_date_2 + timedelta(days=1),  # 16 дней - после первого
            check_out_date=self.future_date_3                      # 20 дней
        )
        
        try:
            booking2.full_clean()  # Не должно вызывать ошибку
            booking2.save()
        except ValidationError:
            pytest.fail("Непересекающиеся бронирования не должны вызывать ошибку")

    def test_booking_string_representation(self):
        """Тест строкового представления бронирования"""
        booking = Booking.objects.create(
            room=self.room,
            check_in_date=self.future_date_1,
            check_out_date=self.future_date_2
        )
        
        # Получите реальное строковое представление для диагностики
        actual_string = str(booking)
        print(f"Реальная строка: '{actual_string}'")
        
        # Ожидаемая строка должна соответствовать реальному __str__ методу
        expected_string = f"Бронирование #{booking.id} - комната #{self.room.id} ({self.future_date_1} - {self.future_date_2})"
        assert str(booking) == expected_string