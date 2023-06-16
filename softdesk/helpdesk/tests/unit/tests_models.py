from django.test import TestCase

from softdesk.account.models import User
from softdesk.helpdesk.models import Project, Contributor


class ProjectTestCase(TestCase):
    def setUp(self) -> None:
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


class ContributorTestCase(TestCase):
    def setUp(self) -> None:
        osy = User.objects.create(username='osynia')
        dazak = User.objects.create(username='dazak')
        fiann = User.objects.create(username='fiann')
        p1 = Project.objects.get(title='Projet 1', author=osy)
        Contributor.objects.create(
            user_contributor=osy,
            project_contributor=p1
        )
        Contributor.objects.create(
            user_contributor=dazak,
            project_contributor=p1,
            permission=Contributor.Permission.READ,
            role=Contributor.Role.MANAGER
        )
        Contributor.objects.create(
            user_contributor=fiann,
            project_contributor=p1,
            permission=Contributor.Permission.READ,
            role=Contributor.Role.CREATOR
        )
        count = Contributor.objects.count()
        self.assertEqual(count, 3)
