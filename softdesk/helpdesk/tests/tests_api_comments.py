from rest_framework import status

from .tests_api_base import ListAPITestCase


class TestComment(ListAPITestCase):

    def setUp(self) -> None:
        super().setUp()
        self.url = '/projects/1/issues/1/comments/'

        # create a new project
        self.api_authentication(self.get_token('dazak', 'password123'))
        response = self.client.post('/projects/', self.p1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # with osynia as manager
        osynia = {
            "user_contributor": 3,
            "project_contributor": 1,
            "permission": "RD",
            "role": "MANG",
        }
        response = self.client.post('/projects/1/users/', osynia)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # create an issue on the project
        issue = {
            'title': 'Issue for test',
            'description': 'Issue testing description',
            'project': 1,
            'author': 2,  # Dazak
            'assignee': 3  # Osynia
        }
        response = self.client.post('/projects/1/issues/', issue)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # prepares a comment for testing
        self.comment = {
            'description': 'Commentaire d''un problème pour le test'
        }

    def test_list(self):
        self.get_list_with_admin_authentification()
        self.get_list_with_author_authentification()
        # the manager can read the comment of another user
        self.client.logout()
        self.api_authentication(self.get_token('dazak', 'password123'))
        response = self.client.post(self.url, self.comment)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.client.logout()
        self.api_authentication(self.get_token('osynia', 'password123'))
        response = self.client.get(self.url)
        data = response.json()["results"]
        self.assertEqual(len(data), 1)

    def test_create(self):

        # not authentificated or somebody that is not a contributor
        # cannot acces the issue : cf. tests_api_issues

        # test creation with the manager
        self.client.logout()
        self.api_authentication(self.get_token('osynia', 'password123'))
        response = self.client.post(self.url, self.comment)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update(self):

        # create a comment with dazak
        self.client.logout()
        self.api_authentication(self.get_token('dazak', 'password123'))
        response = self.client.post(self.url, self.comment)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # update with Osynia a manager
        self.client.logout()
        self.api_authentication(self.get_token('osynia', 'password123'))
        response = self.client.put(self.url+'1/', self.comment)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # update with dazak the author
        self.client.logout()
        self.api_authentication(self.get_token('dazak', 'password123'))
        response = self.client.put(self.url+'1/', self.comment)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete(self):

        # create a comment with dazak
        self.client.logout()
        self.api_authentication(self.get_token('dazak', 'password123'))
        response = self.client.post(self.url, self.comment)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Authentication-based deletion testing
        self.delete_without_authentification()
        self.delete_with_manager_authentification()
        self.delete_with_author_authentification()
