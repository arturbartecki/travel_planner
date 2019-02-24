from rest_framework import serializers, exceptions

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

    trip = serializers.PrimaryKeyRelatedField(
        queryset=Trip.objects.all(),
        many=False
    )

    class Meta:
        model = TripDay
        fields = ('id', 'order', 'trip', 'content')
        read_only_fields = ('id', 'order')

    def validate(self, attrs):
        user = self.context['request'].user
        if attrs['trip'].author == user:
            return attrs
        else:
            raise exceptions.ValidationError()
