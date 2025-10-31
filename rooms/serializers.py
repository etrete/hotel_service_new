from rest_framework import serializers
from .models import HotelRoom


class HotelRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = HotelRoom
        fields = ['id', 'description', 'price_per_night', 'created_at']
        read_only_fields = ['id', 'created_at']


class HotelRoomCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = HotelRoom
        fields = ['description', 'price_per_night']


class HotelRoomListSerializer(serializers.ModelSerializer):
    class Meta:
        model = HotelRoom
        fields = ['id', 'description', 'price_per_night', 'created_at']