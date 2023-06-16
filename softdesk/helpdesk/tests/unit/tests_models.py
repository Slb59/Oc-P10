from django.test import TestCase

from softdesk.account.models import User
from softdesk.helpdesk.models import Project


class ProjectTestCase(TestCase):
    def setUp(self):
        osy = User.objects.create(username='osynia')
        Project.objects.create(
            title='Projet 1',
            description='Tout premier projet',
            type='FRE',
            author=osy
            )

    def test_get_project(self):
        p1 = Project.objects.get(title='Projet 1')
        self.assertEqual(p1.description, 'Tout premier projet')
        self.assertEqual(p1.get_type(), Project.Platform.FRONTEND)
