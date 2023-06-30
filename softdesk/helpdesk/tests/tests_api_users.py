from rest_framework import status

from softdesk.helpdesk.models import Project, Contributor, User
from .tests_api_base import BaseAPITestCase


class TestContributor(BaseAPITestCase):

    def setUp(self) -> None:
        super().setUp()
        self.url = '/projects/1/users/'

        # create new user for adding a creator
        self.user_fiann = User.objects.create_user(
            username='fiann', password='password123'
            )

        # create a new project
        self.api_authentication(self.get_token('admin', 'password123'))
        response = self.client.post('/projects/', self.p1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # with a manager
        project_test = Project.objects.get(id=1)
        Contributor.objects.create(
            user_contributor=self.user_osynia,
            project_contributor=project_test,
            role='MANG'
            )

        self.creator = {
            "user_contributor": 3,
            "project_contributor": 1,
            "permission": "RD",
            "role": "CREA",
        }

    def test_list(self):

        self.get_list_without_autentification()
        self.get_list_with_admin_authentification()

    def test_create(self):

        # Only the author can add a new contributor

        # Authentication credentials were not provided
        self.client.logout()
        response = self.client.post(self.url, self.creator)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # test creation with the manager
        self.client.logout()
        self.api_authentication(self.get_token('osynia', 'password123'))
        response = self.client.post(self.url, self.creator)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # create with the author:admin
        self.client.logout()
        self.api_authentication(self.get_token('admin', 'password123'))
        response = self.client.post(self.url, self.creator)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # create the same contributor
        response = self.client.post(self.url, self.creator)
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update(self):

        # you can't update a contributor, you need to delete it
        # next create a new one

        # without authentification
        self.client.logout()
        response = self.client.put(self.url+'1/', self.creator)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


