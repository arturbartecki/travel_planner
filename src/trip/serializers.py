from rest_framework import serializers

from .models import Trip, TripDay


class TripSerializer(serializers.ModelSerializer):
    """Serialier for Trip object"""

    class Meta:
        model = Trip
        fields = ('id', 'title', 'author', 'description')
        read_only_fields = ('id', 'author')


class TripDetailSerializer(serializers.ModelSerializer):
    """Serializer for trip detail view"""
    # In future detail will contain more info than regular TripSerialzier

    class Meta:
        model = Trip
        fields = ('id', 'title', 'author', 'description')
        read_only_fields = ('id', 'author')


class TripDaySerializer(serializers.ModelSerializer):
    """Serializer for Trip Day object"""

    class Meta:
        model = TripDay
        fields = ('id', 'trip', 'order', 'content')
        read_only_fields = ('id', 'trip', 'order')
