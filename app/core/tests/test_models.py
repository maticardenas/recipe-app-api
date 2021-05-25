from django.test import TestCase
from django.contrib.auth import get_user_model

class ModelTests(TestCase):

    def test_create_user_with_email_successful(self):
        """ Tests creating a new user with an email is successful """
        # given
        email = "test@learning.com"
        password = "Testpass123"

        # when
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        # then
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """ Tests the email for a new user is normalized """
        email = "test@LEARNING.COM"
        password = "Testpass123"

        # when
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        # then
        self.assertEqual(user.email, email.lower())