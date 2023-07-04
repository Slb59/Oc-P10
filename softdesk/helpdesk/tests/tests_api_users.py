from django.db.utils import IntegrityError

from rest_framework import status

from softdesk.helpdesk.models import Project, Contributor
from .tests_api_base import BaseAPITestCase


class TestContributor(BaseAPITestCase):

    def setUp(self) -> None:
        super().setUp()
        self.url = '/projects/1/users/'

        # create a new project
        self.api_authentication(self.get_token('dazak', 'password123'))
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
            "user_contributor": 4,  # fiann
            "project_contributor": 1,
            "permission": "RD",
            "role": "CREA",
        }

    def test_list(self):

        self.get_list_without_autentification()
        self.get_list_with_admin_authentification()
        self.get_list_with_author_authentification()

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

        # create with the author:dazak
        self.client.logout()
        self.api_authentication(self.get_token('dazak', 'password123'))
        response = self.client.post(self.url, self.creator)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update(self):

        # you can't update a contributor, you need to delete it
        # next create a new one

        # without authentification
        self.client.logout()
        response = self.client.put(self.url+'1/', self.creator)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # with dazak authentification
        self.client.logout()
        self.api_authentication(self.get_token('dazak', 'password123'))
        response = self.client.put(self.url+'1/', self.creator)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete(self):

        # without authentification
        self.delete_without_authentification()

        # with manager connection
        self.delete_with_manager_authentification()

        # with dazak : if the author is delete,
        # you must be superuser to create another one
        self.client.logout()
        self.api_authentication(self.get_token('dazak', 'password123'))
        response = self.client.get(self.url)
        data = response.json()["results"]
        self.assertEqual(len(data), 2)
        response = self.client.delete(self.url+'2/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        response = self.client.get(self.url)
        data = response.json()["results"]
        self.assertEqual(len(data), 1)

        # delete the author then verify the project data as admin
        response = self.client.delete(self.url+'1/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        response = self.client.get('/projects/1/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.client.logout()
        self.api_authentication(self.get_token('admin', 'password123'))
        response = self.client.get('/projects/1/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        excepted = {
                'id': 1,
                'title': 'Projet test',
                "description": "Description du projet test",
                "type": "BKE",
                "contributors": [],
                'author': None
            }
        self.assertEqual(excepted, response.json())

    def test_create_author_after_delete(self):
        # login as admin
        self.client.logout()
        self.api_authentication(self.get_token('admin', 'password123'))
        # delete contributors
        response = self.client.delete(self.url+'1/')
        response = self.client.delete(self.url+'2/')
        response = self.client.get(self.url)
        data = response.json()["results"]
        self.assertEqual(len(data), 0)
        # add fiann as author
        self.creator['role'] = 'AUTH'
        response = self.client.post(self.url, self.creator)
        # check the author of the project
        response = self.client.get('/projects/1/')
        contributor_expected = {
            'id': 3, 'user_contributor': 4, 'permission': 'RD', 'role': 'AUTH'
        }
        excepted = {
                'id': 1,
                'title': 'Projet test',
                "description": "Description du projet test",
                "type": "BKE",
                "contributors": [contributor_expected],
                'author': self.user_fiann.id
            }
        self.assertEqual(excepted, response.json())

    def test_create_auhor_as_exists_already_one(self):
        # login as admin
        self.client.logout()
        self.api_authentication(self.get_token('admin', 'password123'))
        # try adding fiann as author
        self.creator['role'] = 'AUTH'
        # response = self.client.post(self.url, self.creator)
        with self.assertRaises(Exception) as raised:
            response = self.client.post(self.url, self.creator)
            print(response.json())  # code not reached ?
        self.assertEqual(IntegrityError, type(raised.exception))
