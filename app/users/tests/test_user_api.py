from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse("user:create")

USER_PAYLOAD = {
            "email": "test@example.com",
            "password": "totalPAssword1234",
        }

def create_user(**params):
    return get_user_model().objects.create_user(**params)

class PublicUserApiTests(TestCase):
    # Test the public user APIs.
    def setUp(self):
        self.client = APIClient
    
    def test_create_valid_user_success(self):
        # Test that a new user is created
        # Arrange

        # Act
        res = self.client.post(CREATE_USER_URL, USER_PAYLOAD)
        user = get_user_model().objects.get(**res.data)

        # Assert
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertTrue(user.check_password(USER_PAYLOAD['password']))
        self.assertNotIn('password', res.data)

    def test_user_exists(self):
        # Test that creating a suplicate user fails
        # Arrange
        create_user(USER_PAYLOAD)

        # Act
        res = self.client.post(CREATE_USER_URL, USER_PAYLOAD) 

        # Assert
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        # Test that the password length requirement is met
        # Arrange
        payload = {"password": "pw"}
        print(payload)
        # Act
        res = self.client.post(CREATE_USER_URL, payload)
