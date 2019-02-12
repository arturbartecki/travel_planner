from rest_framework import serializers

from .models import Trip


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
