"""
    Test for User API
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

USER_REGISTER_URL = reverse('user:register')
USER_LOGIN_URL = reverse('user:login')
USER_DETAIL_URL = reverse('user:detail')
USER_UPDATE_URL = reverse('user:update')
USER_CHANGE_PASSWORD_URL = reverse('user:change-password')

GET_ALL_USER_URL = reverse('user:get-users')


def delete_user_url(user_id):
    """Create and return a user detail url"""
    return reverse('user:delete-user', args=[user_id])


def create_user(**payload):
    """Create and return a user"""
    return get_user_model().objects.create_user(**payload)


class PublicUserAPITest(TestCase):
    """Test unauthenticated user app API request """

    def setUp(self):
        self.client = APIClient()

    def test_user_registration_successful(self):
        """Testing create a new user successfully."""
        payload = {
            'email': 'test@example.com',
            'password': 'test1234'
        }
        res = self.client.post(USER_REGISTER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data['email'], payload['email'])
        self.assertNotIn('password', res.data)

    def test_user_with_email_exists_error(self):
        """Testing return error if user email already exists."""
        payload = {
            'email': 'test@example.com',
            'password': 'testpass123',
        }
        create_user(**payload)

        res = self.client.post(USER_REGISTER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """Testing return error if user given password is too short"""
        payload = {
            'email': 'test@example.com',
            'password': 'test',
        }
        res = self.client.post(USER_REGISTER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(email=payload['email']).exists()
        self.assertFalse(user_exists)

    def test_user_login_successful(self):
        """testing user login successfully and return access and refresh token"""
        payload = {
            'email': 'test@example.com',
            'password': 'test1234',
        }
        create_user(**payload)
        res = self.client.post(USER_LOGIN_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('access', res.data)
        self.assertIn('refresh', res.data)

    def test_user_login_error_with_bad_credentials(self):
        """Testing return error if user given credentials are invalid or not registered """
        create_user(email='test@example.com', password='goodpass')
        payload = {
            'email': 'test@example.com',
            'password': 'test1234',
        }
        res = self.client.post(USER_LOGIN_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_login_error_with_blank_password(self):
        """Testing return error if user login in with blank password"""
        create_user(email='test@example.com', password='goodpass')
        payload = {
            'email': 'test@example.com',
            'password': '',
        }
        res = self.client.post(USER_LOGIN_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('access', res.data)
        self.assertNotIn('refresh', res.data)

    def test_retrieve_user_unauthorized(self):
        """Test authentication is required for users."""
        res = self.client.get(USER_DETAIL_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUserAPITests(TestCase):
    """Test API requests that require authentication."""

    def setUp(self):
        self.user = create_user(
            email='test@example.com',
            password='test1234', )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_user_detail(self):
        """testing retrieve detail for logged in user"""
        res = self.client.get(USER_DETAIL_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['email'], 'test@example.com')

    def test_update_user_successfully(self):
        """testing update logged in user detail successfully"""
        payload = {
            'name': 'Updated name',
            'phone_number': '01515620305'
        }
        res = self.client.put(USER_UPDATE_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['name'], payload['name'])
        self.assertEqual(res.data['phone_number'], payload['phone_number'])

    def test_user_update_error_if_phone_number_exists(self):
        """testing return error if phone_number is already exists"""
        new_user = create_user(email='test2@example.com', password='test12344')
        new_user.phone_number = '01515620305'
        new_user.save()

        payload = {
            'phone_number': '01515620305'
        }
        res = self.client.put(USER_UPDATE_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_change_password_successfully(self):
        """Testing user change password successfully."""
        payload = {
            'old_password': 'test1234',
            'new_password': 'new_password',
            'confirm_password': 'new_password'
        }
        res = self.client.post(USER_CHANGE_PASSWORD_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['msg'], 'Password updated successfully.')
        user = get_user_model().objects.get(id=self.user.id)
        self.assertTrue(user.check_password(payload['new_password']))


class SuperUserAPITests(TestCase):
    """Testing API request for admin users"""

    def setUp(self):
        self.user = create_user(
            email='test@example.com',
            password='test1234', )
        self.user.is_staff = True
        self.user.save()
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_get_all_user_successfully(self):
        """Testing all user detail response by admin user"""
        res = self.client.get(GET_ALL_USER_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_delete_user_successfully(self):
        """Create and delete a user by admin"""
        payload = {
            'email': 'test2@example.com',
            'password': 'test1234',
        }
        user = create_user(**payload)
        url = delete_user_url(user.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
