from rest_framework import status

from softdesk.helpdesk.models import Project, Contributor
from .tests_api_base import ListAPITestCase


class TestProject(ListAPITestCase):

    def setUp(self) -> None:
        super().setUp()
        self.url = '/projects/'

    def format_datetime(self, value):
        return value.strftime("%Y-%m-%dT%H:%M:%S.%fZ")

    def test_list(self):

        # self.get_list_without_autentification()
        self.get_list_with_admin_authentification()
        self.get_list_with_author_authentification()

        # list only the project if contributor
        # create 2 projects
        response = self.client.post(self.url, self.p1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.p1['title'] = 'Projet test 2'
        response = self.client.post(self.url, self.p1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # add osynia as manager of the first project

        project_test = Project.objects.get(id=1)
        Contributor.objects.create(
            user_contributor=self.user_osynia,
            project_contributor=project_test,
            role='MANG'
            )
        # count the projects listing has dazak
        response = self.client.get(self.url)
        data = response.json()["results"]
        self.assertEqual(len(data), 2)
        # count the projects listing has osynia
        self.client.logout()
        self.api_authentication(self.get_token('osynia', 'password123'))
        response = self.client.get(self.url)
        data = response.json()["results"]
        self.assertEqual(len(data), 1)

    def test_create(self):

        self.assertFalse(Project.objects.exists())

        # Authentication credentials were not provided
        response = self.client.post(self.url, self.p1)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # with dazak authentification
        self.api_authentication(self.get_token('dazak', 'password123'))
        response = self.client.post(self.url, self.p1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update(self):

        # post a new project
        self.api_authentication(self.get_token('dazak', 'password123'))
        response = self.client.post(self.url, self.p1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Authentication credentials were not provided
        self.client.logout()
        response = self.client.put(self.url+'1/', self.p1)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # with dazak authentification, the author of p1
        self.api_authentication(self.get_token('dazak', 'password123'))
        response = self.client.put(self.url+'1/', self.p1)
        # self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # with another connected user, not a contributor
        self.client.logout()
        self.api_authentication(self.get_token('osynia', 'password123'))
        response = self.client.put(self.url+'1/', self.p1)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # with another connected user contributor but not author
        project_test = Project.objects.get(id=1)
        Contributor.objects.create(
            user_contributor=self.user_osynia,
            project_contributor=project_test,
            role='MANG'
            )
        self.api_authentication(self.get_token('osynia', 'password123'))
        response = self.client.put(self.url+'1/', self.p1)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete(self):

        # post a new project
        self.api_authentication(self.get_token('dazak', 'password123'))
        response = self.client.post(self.url, self.p1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Authentication credentials were not provided
        self.client.logout()
        response = self.client.delete(self.url+'1/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # with another connected user contributor but not author
        project_test = Project.objects.get(id=1)
        Contributor.objects.create(
            user_contributor=self.user_osynia,
            project_contributor=project_test,
            role='MANG'
            )
        self.api_authentication(self.get_token('osynia', 'password123'))
        response = self.client.delete(self.url+'1/')
        # self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # with dazak authentification, the author of p1
        self.api_authentication(self.get_token('dazak', 'password123'))
        response = self.client.delete(self.url+'1/')
        # self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
