from rest_framework.test import APITestCase

from .models import User


class UserApiTestCase(APITestCase):

    def setUp(self) -> None:
        self.user = User.objects.create(username="test", password="test")
        return super().setUp()

    def test_getusers(self):
        self.client.login(username="test", password="test")
        ...
        # test without authentification
        # test with authentification
