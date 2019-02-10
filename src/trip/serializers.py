from rest_framework import serializers

from .models import Trip


class TripSerializer(serializers.ModelSerializer):
    """Serialier for Trip object"""

    class Meta:
        model = Trip
        fields = ('title', 'author', 'description')
