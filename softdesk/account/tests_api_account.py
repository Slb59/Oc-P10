from django.db.utils import IntegrityError
from rest_framework.test import APITestCase
from rest_framework import status


from .models import User


class TestUser(APITestCase):

    def setUp(self) -> None:

        super().setUp()

        # create a user for login testing
        self.user_osynia = User.objects.create_user(
            username='osynia', password='password123',
            birth_date='1970-01-01'
            )

        self.user_osynia_dict = {
            "username": "osynia",
            "password": "password123",
            "birth_date": "1970-01-01"
        }

    def authentifacated_as_osynia(self):
        response = self.client.post('/login/', self.user_osynia_dict)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)

    def test_login(self):

        response = self.client.login(username="osynia", password="password123")
        self.assertEqual(response, True)

        response = self.client.post('/login/', self.user_osynia_dict)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertTrue("access" in response.data)
        self.assertTrue("refresh" in response.data)

    def test_signup_list(self):

        # you must be authentificated for getting list of users
        response = self.client.get('/signup/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # get token as osynia
        self.authentifacated_as_osynia()

        # get list of users
        response = self.client.get('/signup/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()["results"]
        self.assertEqual(len(data), 1)

    def test_signup_create(self):

        # anybody can create a new user
        new_user = {
            "username": "test",
            "first_name": "test",
            "last_name": "test",
            "email": "test@example.com",
            "password": "password123",
            "post_description": "Le travail de test",
            "birth_date": '1970-01-01'
        }
        response = self.client.post('/signup/', new_user)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_signup_create_minus15yearsold(self):

        # age must be > 15
        new_user = {
            "username": "test2",
            "first_name": "test2",
            "last_name": "test2",
            "email": "test2@example.com",
            "password": "password123",
            "post_description": "Le travail de test",
            "birth_date": '2023-01-01'
        }
        with self.assertRaises(Exception) as raised:
            self.client.post('/signup/', new_user)
        self.assertEqual(IntegrityError, type(raised.exception))

    def test_signup_get(self):

        # you must be authentificated for getting a user information
        response = self.client.get('/signup/1/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.authentifacated_as_osynia()
        response = self.client.get('/signup/1/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        excepted = {
                'id': 1,
                'username': 'osynia',
                "first_name": '',
                'last_name': '',
                'email': '',
                'post_description': '',
                "birth_date": '1970-01-01',
                'is_superuser': False
            }
        self.assertEqual(excepted, response.json())

    def test_signup_update(self):

        # you must be authentificated for updating a user information
        self.user_osynia_dict['email'] = 'osynia@example.com'
        response = self.client.put('/signup/1/', self.user_osynia_dict)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.authentifacated_as_osynia()
        response = self.client.put('/signup/1/', self.user_osynia_dict)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # test update another user => forbidden
        self.test_signup_create()
        self.authentifacated_as_osynia()
        new_user = {
            "username": "J5nwS",
            "first_name": "string",
            "last_name": "string",
            "email": "user@example.com",
            "post_description": "string",
            "birth_date": '1970-01-01',
            "is_superuser": True
        }
        response = self.client.put('/signup/2/', new_user)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # test update another user ok if osynia is superuser
        self.user_osynia_dict['is_superuser'] = True
        response = self.client.put('/signup/1/', self.user_osynia_dict)
        self.authentifacated_as_osynia()
        new_user = {
            "username": "J5nwS",
            "first_name": "string",
            "last_name": "string",
            "email": "user@example.com",
            "post_description": "string",
            "birth_date": '1970-01-01',
            "is_superuser": True
        }
        response = self.client.put('/signup/2/', new_user)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_signup_delete(self):

        # you must be authentificated for deleting a user
        response = self.client.delete('/signup/1/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # connect as a superuser
        self.authentifacated_as_osynia()
        self.user_osynia_dict['is_superuser'] = True
        self.user_osynia_dict['email'] = 'osynia@example.com'
        response = self.client.put('/signup/1/', self.user_osynia_dict)
        self.test_signup_create()
        self.authentifacated_as_osynia()
        response = self.client.delete('/signup/2/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
