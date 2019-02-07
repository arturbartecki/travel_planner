from django.test import TestCase

from trip import models

class TripModelTests(TestCase):
    """Test Trip model"""

    def test_trip_str(self):
        """Test trip model string representation"""
        trip = models.Trip.objects.create(
            title='Test Title',
            description='Trip object test'
        )

        self.assertEqual(trip.title, str(trip))