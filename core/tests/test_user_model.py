"""
    Tests for User Model
"""
from django.test import TestCase
from django.contrib.auth import get_user_model


class UserModelTest(TestCase):
    """Test user model"""

    def test_create_user_with_email_successful(self):
        """Test creating a user with email is successful"""
        email = "test@example.com"
        password = 'test12345'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_user_email_normalized(self):
        """Test email is normalized for new user"""
        sample_emails = [
            ['test1@EXAMPLE.com', 'test1@example.com'],
            ['test2@EXAMPLE.COM', 'test2@example.com'],
            ['Test3@Example.com', 'Test3@example.com'],
            ['test4@EXAMPLE.com', 'test4@example.com'],
        ]
        for email, expected in sample_emails:
            user = get_user_model().objects.create_user(email, 'test1234')
            self.assertEqual(user.email, expected)

    def test_user_without_email_raise_errors(self):
        """Test create a user without email and raise a valueError"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('', 'test1234')
