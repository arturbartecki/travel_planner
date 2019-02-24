from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APIClient

from trip.models import Trip, TripDay
from trip.serializers import TripSerializer, TripDetailSerializer

TRIPS_URL = reverse('trip:trip-list')
TRIP_DAYS_URL = reverse('trip:tripday-list')


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


def get_trip_detail_url(trip_id):
    return reverse('trip:trip-detail', args=[trip_id])


class PublicTripApiTest(TestCase):
    """Test unauthenticated trip API access"""

    def setUp(self):
        self.user = sample_user()
        self.client = APIClient()

    def test_public_list_trips(self):
        """Test retrieving list of public trips"""
        Trip.objects.create(
            title='Test title',
            author=self.user,
            description='Test description',
            is_public=False,
        )
        Trip.objects.create(
            title='2nd object',
            author=self.user,
            description='Test description',
        )

        res = self.client.get(TRIPS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)

    def test_public_detail_private_trip(self):
        """Test if unauthorized user can view trip with is_public=False"""
        trip = Trip.objects.create(
            title='Test title',
            author=self.user,
            description='Test desc',
            is_public=False
        )

        url = get_trip_detail_url(trip.id)
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    def test_public_detail_public_trip(self):
        """Test if unauthorized user can view trip with is_public=True"""
        trip = Trip.objects.create(
            title='Test title',
            author=self.user,
            description='Test desc'
        )
        url = get_trip_detail_url(trip.id)
        res = self.client.get(url)

        serializer = TripDetailSerializer(trip)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(serializer.data, res.data)

    def test_public_create_trip(self):
        """Test if trip can be created as not authenticated user"""
        payload = {
            'title': 'Test title',
            'author': self.user,
            'description': 'Test description'
        }

        res = self.client.post(TRIPS_URL, payload)
        trips = Trip.objects.all()

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(len(trips), 0)

    def test_public_partial_update_trip(self):
        """Test if unauthorized user can update trip with patch"""
        trip = Trip.objects.create(
            title='Test title',
            author=self.user,
            description='Test desc'
        )

        payload = {
            'title': 'New title'
        }

        url = get_trip_detail_url(trip.id)
        res = self.client.patch(url, payload)
        trip.refresh_from_db()

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertNotEqual(trip.title, payload['title'])

    def test_public_full_update_trip(self):
        """Test if unauthorized user can update trip with put"""
        trip = Trip.objects.create(
            title='Test title',
            author=self.user,
            description='Test desc'
        )

        payload = {
            'title': 'New title',
            'author': self.user,
            'description': 'New description'
        }

        url = get_trip_detail_url(trip.id)
        res = self.client.put(url, payload)
        trip.refresh_from_db()

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertNotEqual(trip.title, payload['title'])
        self.assertNotEqual(trip.description, payload['description'])

    def test_public_delete_trip(self):
        """Test if unauthorized user can delete trip"""
        trip = Trip.objects.create(
            title='Test title',
            author=self.user,
            description='test desc'
        )
        url = get_trip_detail_url(trip.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateTripApiTest(TestCase):
    """Test authenticated trip API access"""

    def setUp(self):
        self.client = APIClient()
        self.user = sample_user()
        self.client.force_authenticate(self.user)

    # Test trips with author == request.user

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

    def test_trip_detail_view(self):
        """Test viewing trip detail"""
        trip = Trip.objects.create(
            title='Test title',
            author=self.user,
            description='Test desc'
        )

        url = get_trip_detail_url(trip.id)
        res = self.client.get(url)

        serializer = TripDetailSerializer(trip)

        self.assertEqual(serializer.data, res.data)

    def test_partial_update_trip(self):
        """Test updating trip with PATCH"""
        trip = Trip.objects.create(
            title='Test title',
            author=self.user,
            description='Test description'
        )

        payload = {
            'title': 'New title'
        }

        url = get_trip_detail_url(trip.id)
        res = self.client.patch(url, payload)

        trip.refresh_from_db()

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(trip.title, payload['title'])

    def test_full_update_trip(self):
        """Test updating trip with PUT"""

        trip = Trip.objects.create(
            title='Test title',
            author=self.user,
            description='Test desc'
        )
        payload = {
            'title': 'New title',
            'author': self.user,
            'description': 'New description'
        }

        url = get_trip_detail_url(trip.id)
        res = self.client.put(url, payload)

        trip.refresh_from_db()

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(trip.title, payload['title'])
        self.assertEqual(trip.author, payload['author'])
        self.assertEqual(trip.description, payload['description'])

    def test_delete_trip(self):
        """Test deleting trip"""
        trip = Trip.objects.create(
            title='Test title',
            author=self.user,
            description='Test desc'
        )
        trips = Trip.objects.all()

        self.assertEqual(len(trips), 1)

        url = get_trip_detail_url(trip.id)
        self.client.delete(url)

        trips = Trip.objects.all()
        self.assertEqual(len(trips), 0)

    # Test trips with author != request.user

    def test_noauthor_create_trip(self):
        """Test if user can create trip and assign other user to author """
        user2 = sample_user(email='testvalid@email.com')

        payload = {
            'title': 'test title',
            'author': user2,
            'description': 'Test desc'
        }

        res = self.client.post(TRIPS_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        # Check if trip author is changed to request.user
        trip = Trip.objects.get(title=payload['title'])
        self.assertEqual(trip.author, self.user)

    def test_notauthor_private_trip_detail_view(self):
        """Test if user can see private trip details """
        user2 = sample_user(email='testvalid@email.com')

        trip = Trip.objects.create(
            title='Test title',
            author=user2,
            description='Test description',
            is_public=False
        )

        url = get_trip_detail_url(trip.id)
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    def test_noauthor_partial_update_trip(self):
        """Test if user can update other user trip using PATCH"""
        user2 = sample_user(email='testvalid@email.com')
        trip = Trip.objects.create(
            title='Test title',
            author=user2,
            description='Test description'
        )

        payload = {
            'title': 'New title'
        }

        url = get_trip_detail_url(trip.id)
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_noauthor_full_update_trip(self):
        """Test if user can update other user trip using PUT """
        user2 = sample_user(email='testvalid@email.com')
        trip = Trip.objects.create(
            title='Test title',
            author=user2,
            description='Test description'
        )

        payload = {
            'title': 'New title',
            'description': 'New description'
        }

        url = get_trip_detail_url(trip.id)
        res = self.client.put(url, payload)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_noauthor_delete_trip(self):
        """Test if user can delete other user trip """
        user2 = sample_user(email='testvalid@email.com')
        trip = Trip.objects.create(
            title='Test title',
            author=user2,
            description='Test description'
        )

        url = get_trip_detail_url(trip.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class PublicTripDayApiTest(TestCase):
    """Test unauthenticated trip day API access"""

    def setUp(self):
        self.client = APIClient()
        self.user = sample_user()
        self.trip = Trip.objects.create(
            title='Test title',
            author=self.user,
            description='Test description'
        )
        self.private_trip = Trip.objects.create(
            title='Private title',
            author=self.user,
            description='Private description',
            is_public=False
        )

    def test_public_list_trip_days(self):
        """Test public trip days list"""
        TripDay.objects.create(
            trip=self.trip,
            content='Test content'
        )
        TripDay.objects.create(
            trip=self.trip,
            content='Test content 2'
        )
        TripDay.objects.create(
            trip=self.private_trip,
            content='Test content'
        )

        res = self.client.get(TRIP_DAYS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 2)


class PrivateTripDayApiTest(TestCase):
    """Test trip day api as authenticated user"""

    def setUp(self):
        self.user = sample_user()
        self.client = APIClient()
        self.client.force_authenticate(self.user)
        self.trip = Trip.objects.create(
            title='Test title',
            author=self.user,
            description='Test description'
        )
        self.private_trip = Trip.objects.create(
            title='Private title',
            author=self.user,
            description='Private description',
            is_public=False
        )

    def test_private_list_trip_days(self):
        """Test if trip days list is correct"""
        TripDay.objects.create(
            trip=self.trip,
            content='Test content'
        )
        TripDay.objects.create(
            trip=self.trip,
            content='Test content 2'
        )
        TripDay.objects.create(
            trip=self.trip,
            content='Test content'
        )
        res = self.client.get(TRIP_DAYS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 3)

    def test_private_list_private_trip_days(self):
        """If other user's private trip days are listed"""
        TripDay.objects.create(
            trip=self.trip,
            content='Test content'
        )
        user2 = sample_user(email='anothervalid@email.com')
        private_trip = Trip.objects.create(
            title='Private title',
            author=user2,
            description='Private desc'
        )
        TripDay.objects.create(
            trip=private_trip,
            content='Private content'
        )

        res = self.client.get(TRIP_DAYS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 2)

    def test_create_trip_day_when_not_trip_author(self):
        """Test if user can create trip_day while not being trip author"""
        user2 = sample_user(email='another@valid.com')
        private_trip = Trip.objects.create(
            title='Private title',
            author=user2,
            description='Private desc'
        )
        payload = {
            'content': 'Test content',
            'trip': f'{private_trip.id}'
        }

        res = self.client.post(TRIP_DAYS_URL, payload)
        queryset = TripDay.objects.all()

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(len(queryset), 0)
