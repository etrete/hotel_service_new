Hotel Booking Service - Документация

О проекте

Веб-сервис для управления номерами отеля и бронированиями с REST API и веб-интерфейсом.

Технологический стек
Backend: Django + Django REST Framework

Database: PostgreSQL / SQLite

Frontend: Django Templates + Bootstrap

Containerization: Docker + Docker Compose

Testing: pytest путь к файлу/

Запуск проекта 
docker-compose up --build

Доступные URL
Веб-интерфейс
http://localhost:8000/ - Главная страница

http://localhost:8000/rooms/ - Управление номерами

http://localhost:8000/bookings/ - Управление бронированиями

http://localhost:8000/admin/ - Админка Django

REST API Endpoints
text
GET    /api/rooms/list/              # Список номеров
POST   /api/rooms/                   # Создать номер
DELETE /api/rooms/{id}/delete/       # Удалить номер

POST   /api/bookings/                # Создать бронь
GET    /api/bookings/{id}/           # Детали брони
DELETE /api/bookings/{id}/delete/    # Удалить бронь
GET    /api/rooms/{id}/bookings/     # Бронирования номера
GET    /api/availability/{id}/       # Проверить доступность

Особенности реализации
Валидации бронирований
Проверка пересечения дат

Дата выезда > даты заезда

Даты не в прошлом

Номер существует

Сортировка и фильтрация
Сортировка номеров по цене/дате

Сортировка бронирований по дате заезда

Фильтрация активных номеров## New Features
