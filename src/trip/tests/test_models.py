from django.test import TestCase
from django.contrib.auth import get_user_model
from trip.models import Trip, TripDay


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


class TripDayModelTests(TestCase):
    """Test Trip day model"""

    def setUp(self):
        self.user = get_user_model().objects.create(
            email='valid@test.email.com',
            password='testpassword'
        )
        self.trip = Trip.objects.create(
            title='Test title',
            author=self.user,
            description='Test description'
        )

    def test_day_trip_str(self):
        """Test trip day model string representation"""

        trip_day = TripDay.objects.create(
            trip=self.trip,
            content='Basic plans for a day'
        )

        self.assertEqual(
            f'Day {trip_day.order + 1} in trip {trip_day.trip}',
            str(trip_day)
        )

    def test_auto_generating_order_field(self):
        """Test if order field generates valid values"""
        trip_2 = Trip.objects.create(
            title='title test',
            author=self.user,
            description='Test data'
        )
        trip_day_1 = TripDay.objects.create(
            trip=self.trip,
            content='Test content'
        )
        trip_day_2 = TripDay.objects.create(
            trip=self.trip,
            content='Test content'
        )
        diff_trip_day_1 = TripDay.objects.create(
            trip=trip_2,
            content='Test content'
        )

        self.assertEqual(trip_day_1.order, 0)
        self.assertEqual(trip_day_2.order, 1)
        self.assertEqual(diff_trip_day_1.order, 0)

    def test_updating_auto_generated_order_field(self):
        """Test if order value is updated properly"""
        trip_day_1 = TripDay.objects.create(
            trip=self.trip,
            content='Test content 1'
        )
        trip_day_2 = TripDay.objects.create(
            trip=self.trip,
            content='Test content 2'
        )
        trip_day_3 = TripDay.objects.create(
            trip=self.trip,
            content='Test content 3'
        )
        trip_day_3.to(0)
        trip_day_1.refresh_from_db()
        trip_day_2.refresh_from_db()
        trip_day_3.refresh_from_db()

        self.assertEqual(trip_day_1.order, 1)
        self.assertEqual(trip_day_2.order, 2)
        self.assertEqual(trip_day_3.order, 0)
