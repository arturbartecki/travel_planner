from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APIClient

from trip.models import Trip
from trip.serializers import TripSerializer

TRIPS_URL = reverse('trip:trip-list')


def sample_user(
    email='valid@testemail.com',
    password='testpassword',
    name='Test name'
):
    return get_user_model().objects.create(
        email=email,
        password=password,
        name=name
    )


class PublicTripApiTest(TestCase):
    """Test unauthenticated trip API access"""

    def setUp(self):
        self.client = APIClient()

    def test_list_public_trips(self):
        """Test retrieving list of public trips"""
        user = sample_user()
        Trip.objects.create(
            title='Test title',
            author=user,
            description='Test description',
            is_public=False,
        )
        Trip.objects.create(
            title='2nd object',
            author=user,
            description='Test description',
        )

        res = self.client.get(TRIPS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
    
    def test_create_trip_unauthenticated(self):
        """Test if trip can be created as not authenticated user"""
        user = sample_user()
        payload = {
            'title': 'Test title',
            'author': user,
            'description': 'Test description'
        }

        res = self.client.post(TRIPS_URL, payload)
        trips = Trip.objects.all()

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(len(trips), 0)


class PrivateTripApiTest(TestCase):
    """Test authenticated trip API access"""

    def setUp(self):
        self.client = APIClient()
        self.user = sample_user()
        self.client.force_authenticate(self.user)

    def test_retrieve_trips(self):
        """Test retrieving trips filtered by is_public"""
        user2 = sample_user(email='test@validemail.com')
        trip1 = Trip.objects.create(
            title='Test 1',
            author=self.user,

        )
        trip2 = Trip.objects.create(
            title='Test 2',
            author=user2,
        )
        # This trip shouldn't be visible for test request user
        trip3 = Trip.objects.create(
            title='Test 3',
            author=user2,
            is_public=False
        )

        res = self.client.get(TRIPS_URL)

        serializer1 = TripSerializer(trip1)
        serializer2 = TripSerializer(trip2)
        serializer3 = TripSerializer(trip3)

        self.assertIn(serializer1.data, res.data)
        self.assertIn(serializer2.data, res.data)
        self.assertNotIn(serializer3.data, res.data)
        self.assertEqual(len(res.data), 2)
    
    def test_create_valid_trip(self):
        """Test if authenticated user can create trip"""
        payload = {
            'title': 'Test title 1',
            # Author should be added automatically
            'description': 'Test description'
        }
        res = self.client.post(TRIPS_URL, payload)
        trips = Trip.objects.all()

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(trips), 1)
    
    def test_create_invalid_trip(self):
        """Test if authenticated user can create trip with invalid data"""
        res = self.client.post(TRIPS_URL, {'title': ''})
        trip = Trip.objects.all()

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(len(trip), 0)
