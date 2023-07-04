from django.test import TestCase
from django.db.utils import IntegrityError

from softdesk.account.models import User
from softdesk.helpdesk.models import Project, Contributor
from softdesk.helpdesk.models import Issue, Comment


class BaseModelTestCase(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        super(BaseModelTestCase, cls).setUpClass()
        cls.osy = User(username='osynia')
        cls.dazak = User(username='dazak')
        cls.fiann = User(username='fiann')
        cls.p1 = Project(
            title='Projet 1',
            description='Tout premier projet',
            type='FRE',
            # author=cls.osy
            )


class ProjectTestCase(BaseModelTestCase):
    def setUp(self) -> None:
        self.osy.save()
        self.p1.save()

    def test_get_project(self):
        p = Project.objects.get(title='Projet 1')
        self.assertEqual(p.description, 'Tout premier projet')
        self.assertEqual(p.get_type(), Project.Platform.FRONTEND)


class ContributorTestCase(BaseModelTestCase):
    def setUp(self) -> None:
        self.osy.save()
        self.dazak.save()
        self.fiann.save()
        self.p1.save()

        Contributor.objects.create(
            user_contributor=self.osy,
            project_contributor=self.p1  # only one author ?
        )
        Contributor.objects.create(
            user_contributor=self.dazak,
            project_contributor=self.p1,
            permission=Contributor.Permission.READ,
            role=Contributor.Role.MANAGER  # only one manager ?
        )
        Contributor.objects.create(
            user_contributor=self.fiann,
            project_contributor=self.p1,
            permission=Contributor.Permission.READ,
            role=Contributor.Role.CREATOR  # only one creator ?
        )

    def test_count_contributor(self):
        count = Contributor.objects.count()
        self.assertEqual(count, 3)

    def test_unique_constrainte(self):
        with self.assertRaises(Exception) as raised:
            Contributor.objects.create(
                user_contributor=self.fiann,
                project_contributor=self.p1,
                permission=Contributor.Permission.READ,
                role=Contributor.Role.CREATOR  # only one creator ?
            )
        self.assertEqual(IntegrityError, type(raised.exception))


class IssueTestCase(BaseModelTestCase):

    def setUp(self) -> None:
        self.osy.save()
        self.p1.save()

        Issue.objects.create(
            title='Impossible to connect',
            description="Error in connection, my password is not recognized",
            priority=Issue.Priority.HIGH,
            project=self.p1,
            author=self.osy,  # author must be a contributor
            assignee=self.osy  # =author by default
        )

    def test_get_issue(self):
        issue1 = Issue.objects.get(title='Impossible to connect')
        self.assertEqual(issue1.author, self.osy)


class CommentTestCase(BaseModelTestCase):

    def setUp(self) -> None:
        self.osy.save()
        self.p1.save()
        issue = Issue(
            title='Impossible to connect',
            description="Error in connection, my password is not recognized",
            priority=Issue.Priority.HIGH,
            project=self.p1,
            author=self.osy,  # author must be a contributor
            assignee=self.osy  # =author by default
            )
        issue.save()

        Comment.objects.create(
            description='Please use reinit your password link',
            author=self.osy,
            issue=issue
            )

    def test_get_comment(self):
        comment = Comment.objects.get(author=self.osy)
        self.assertEqual(
            comment.description, 'Please use reinit your password link'
            )
        self.assertEqual(
            1, len(Comment.objects.filter(description__startswith='Please'))
            )
