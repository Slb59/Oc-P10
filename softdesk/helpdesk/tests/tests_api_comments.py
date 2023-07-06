from rest_framework import status

from .tests_api_base import BaseAPITestCase


class TestComment(BaseAPITestCase):

    def setUp(self) -> None:

        self.url = '/projects/1/issues/1/comment/'

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
        response = self.client.post('/projects/1/', osynia)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # create an issue on the project
        issue = {
            'title': 'Issue for test',
            'description': 'Issue testing description',
            'project': 1,
            'author': 2,  # Dazak
            'assignee': 3  # Osynia
        }
        response = self.client.post('/projects/1/', issue)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # prepares a comment for testing
        self.comment = {
            'description': 'Commentaire d''un problème pour le test'            
        }
        return super().setUp()

    def test_list(self):
        self.get_list_without_autentification()
        self.get_list_with_admin_authentification()
        self.get_list_with_author_authentification()
