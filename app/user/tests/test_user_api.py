from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

# Test client to API requests and check response
from rest_framework.test import APIClient
# Default status codes
from rest_framework import status

CREATE_USER_URL = reverse("user:create")

def create_user(**params):
    return get_user_model().objects.create_user(**params)


# EACH TEST REFRESHES THE DB, SO THERE IS NO PROBLEM IF WE CREATE THE SAME USER IN EACH OF THEM
class PublicUserAPITests(TestCase):
    """ Tests the users API (public) """

    def setUp(self):
        self.client = APIClient()

    def test_create_valid_user_success(self):
        """ Test creating user with valid payload is successful """
        # given
        payload = {
            "email": "test@learning.com",
            "password": "testpass",
            "name": "Test name"
        }

        # when
        res = self.client.post(CREATE_USER_URL, payload)

        # then
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(payload["password"]))
        self.assertNotIn("password", res.data)


    def test_user_exists(self):
        """ Test creating a user that already exists """
        # given
        payload = {
            "email": "test@learning.com",
            "password": "testpass",
            "name": "Test name"
        }
        create_user(**payload)

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """ Test that the password must be more than 5 characters """
        payload = {
            "email": "test@learning.com",
            "password": "pw",
            "name": "Test name"
        }

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload["email"]
        )
        self.assertFalse(user_exists)
