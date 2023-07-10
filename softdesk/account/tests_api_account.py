from rest_framework.test import APITestCase
from rest_framework import status

from .models import User


class TestUser(APITestCase):

    def setUp(self) -> None:

        # create a user for login testing
        self.user_osynia = User.objects.create_user(
            username='osynia', password='password123'
            )

        return super().setUp()

    def test_login(self):

        response = self.client.login(username="osynia", password="password123")
        self.assertEqual(response, True)

        user_test = {
            "username": "osynia",
            "password": "password123"
        }
        response = self.client.post('/login/', user_test)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertTrue("access" in response.data)
        self.assertTrue("refresh" in response.data)

    def test_signup_get(self):
        self.assertTrue(False)
