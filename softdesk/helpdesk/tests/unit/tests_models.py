from django.test import TestCase

from softdesk.account.models import User
from softdesk.helpdesk.models import Project, Contributor
from softdesk.helpdesk.models import Issue


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
        Project.objects.create(
            title='Projet 1',
            description='Tout premier projet',
            type='FRE',
            author=osy
            )
        p1 = Project.objects.get(title='Projet 1', author=osy)
        Contributor.objects.create(
            user_contributor=osy,
            project_contributor=p1  # only one author ?
        )
        Contributor.objects.create(
            user_contributor=dazak,
            project_contributor=p1,
            permission=Contributor.Permission.READ,
            role=Contributor.Role.MANAGER  # only one manager ?
        )
        Contributor.objects.create(
            user_contributor=fiann,
            project_contributor=p1,
            permission=Contributor.Permission.READ,
            role=Contributor.Role.CREATOR  # only one creator ?
        )
    
    def test_count_contributor(self):
        count = Contributor.objects.count()
        self.assertEqual(count, 3)


class IssueTestCase(TestCase):

    def setUp(self) -> None:
        osy = User.objects.create(username='osynia')
        Project.objects.create(
            title='Projet 1',
            description='Tout premier projet',
            type='FRE',
            author=osy
            )
        p1 = Project.objects.get(title='Projet 1')
        Issue.objects.create(
            title='Impossible to connect',
            description="Error in connection, my password is not recognized",
            priority=Issue.Priority.HIGH,
            project=p1,
            author=osy,  # author must be a contributor
            assignee=osy  # =author by default
        )

    def test_get_issue(self):
        osy = User.objects.get(username='osynia')
        issue1 = Issue.objects.get(title='Impossible to connect')
        self.assertEqual(issue1.author, osy)
