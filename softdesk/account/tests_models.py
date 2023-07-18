from django.test import TestCase
from django.db.utils import IntegrityError


from .models import User


class UserTestCase(TestCase):

    @classmethod
    def setUpTestData(cls) -> None:
        # Create a user
        testuser1 = User.objects.create_user(
            username='testuser1', password='98765abc',
            email='testuser1@gmail.com',
            post_description='Description',
            birth_date='1970-01-01'
            )
        testuser1.save()
        return super().setUpTestData()

    def test_user_content(self):
        user = User.objects.get(username='testuser1')
        email = f'{user.email}'
        post_description = f'{user.post_description}'
        self.assertEqual(email, 'testuser1@gmail.com')
        self.assertEqual(post_description, 'Description')

    def test_user_minus15years(self):
        with self.assertRaises(Exception) as raised:
            User.objects.create_user(
                username='testuser2', password='98765abc',
                email='testuser2@gmail.com',
                post_description='Description',
                birth_date='2023-01-01'
            )
        self.assertEqual(IntegrityError, type(raised.exception))
