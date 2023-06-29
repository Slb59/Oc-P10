from rest_framework import status

from .models import User, Project, Contributor
from .tests_api_base import BaseAPITestCase


class TestContributor(BaseAPITestCase):

    def setUp(self) -> None:
        super().setUp()
        self.url = '/projects/1/users'

        