from django.test import TestCase
from django.contrib.auth import get_user_model


def sample_user(email='test@testdata.com', password='testpassword'):
    return get_user_model().objects.create_user(email, password)


class UserModelTests(TestCase):

    def test_create_user_with_email_successful(self):
        """Test creating a new user with an email is successful"""
        email = 'valid@testdata.com'
        password = 'validpassword123'
        user = sample_user(email=email, password=password)

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test the email for a new user is normalized"""
        email = 'test@TESTDATA.com'
        user = sample_user(email=email)
        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """Test creating user with no email raises error"""
        with self.assertRaises(ValueError):
            sample_user(email=None)

    def test_create_new_superuser(self):
        """ Test creating new superuser"""
        user = get_user_model().objects.create_superuser(
            'superuser@testdata.com',
            'superpassword123'
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
