# from django.urls import reverse_lazy
from rest_framework.test import APITestCase
from rest_framework import status

from .models import User


class BaseAPITestCase(APITestCase):

    def get_token(self, username=None, password=None, access=True):
        username = self.username if (username is None) else username
        password = self.password if (password is None) else password

        # url = reverse_lazy("token_obtain_pair")
        url = '/login/'
        resp = self.client.post(
            url, {"username": username, "password": password}, format="json"
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertTrue("access" in resp.data)
        self.assertTrue("refresh" in resp.data)
        token = resp.data["access"] if access else resp.data["refresh"]
        return token

    def api_authentication(self, token=None):
        token = self.token if (token is None) else token
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)


class TestProject(BaseAPITestCase):

    def setUp(self) -> None:
        self.user_admin = User.objects.create_user(
            username='admin', password='password123'
            )
        self.user_admin.save()
        self.user_admin.is_superuser = True
        self.user_admin.save()

    def format_datetime(self, value):
        return value.strftime("%Y-%m-%dT%H:%M:%S.%fZ")

    def test_list(self):

        response = self.client.get('/projects/')
        # Authentication credentials were not provided
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # with admin authentification
        self.api_authentication(self.get_token('admin', 'password123'))
        response = self.client.get('/projects/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
