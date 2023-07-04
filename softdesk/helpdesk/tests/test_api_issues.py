from .tests_api_base import BaseAPITestCase

from rest_framework import status

from softdesk.helpdesk.models import Project, Contributor


class TestIssue(BaseAPITestCase):

    def setUp(self) -> None:
        super().setUp()
        self.url = '/projects/1/issues/'

        # create a new project
        self.api_authentication(self.get_token('dazak', 'password123'))
        response = self.client.post('/projects/', self.p1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # with osynia as a manager
        project_test = Project.objects.get(id=1)
        Contributor.objects.create(
            user_contributor=self.user_osynia,
            project_contributor=project_test,
            role='MANG'
            )

        self.issue = {
            'title': 'Issue for test',
            'description': 'Issue testing description',
            'project': 1,
            'author': 2,  # Dazak
            'assignee': 3  # Osynia
        }

    def test_list(self):
        self.get_list_without_autentification()
        self.get_list_with_admin_authentification()
        self.get_list_with_author_authentification()

    def test_create(self):

        # Authentication credentials were not provided
        self.client.logout()
        response = self.client.post(self.url, self.issue)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # or somebody that is not a contributor
        self.api_authentication(self.get_token('fiann', 'password123'))
        response = self.client.post(self.url, self.issue)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # test creation with the manager
        self.client.logout()
        self.api_authentication(self.get_token('osynia', 'password123'))
        response = self.client.post(self.url, self.issue)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update(self):

        # create an issue with dazak
        self.client.logout()
        self.api_authentication(self.get_token('dazak', 'password123'))
        response = self.client.post(self.url, self.issue)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # without authentification
        self.client.logout()
        response = self.client.put(self.url+'1/', self.issue)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # update with Osynia a manager
        self.client.logout()
        self.api_authentication(self.get_token('osynia', 'password123'))
        response = self.client.put(self.url+'1/', self.issue)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # update with dazak, the author
        self.client.logout()
        self.api_authentication(self.get_token('osynia', 'password123'))
        response = self.client.put(self.url+'1/', self.issue)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete(self):

        # create an issue with dazak
        self.client.logout()
        self.api_authentication(self.get_token('dazak', 'password123'))
        response = self.client.post(self.url, self.issue)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Authentication-based deletion testing
        self.delete_without_authentification()
        self.delete_with_manager_authentification()
        self.delete_with_author_authentification()


