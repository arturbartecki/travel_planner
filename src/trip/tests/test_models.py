from django.test import TestCase
from django.contrib.auth import get_user_model
from trip.models import Trip


class TripModelTests(TestCase):
    """Test Trip model"""

    def test_trip_str(self):
        """Test trip model string representation"""
        user = get_user_model().objects.create(
            email='valid@testemail.com',
            password='testpassword'
        )
        trip = Trip.objects.create(
            title='Test Title',
            author=user,
            description='Trip object test'
        )

        self.assertEqual(trip.title, str(trip))
