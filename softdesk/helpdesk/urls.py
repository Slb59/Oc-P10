from django.urls import path, include
from rest_framework_nested import routers

from .views_project import ProjectViewSet
from .views_project import ContributorViewSet
from .views_issue import IssueViewSet

app_name = "helpdesk"

helpdesk_router = routers.SimpleRouter()
helpdesk_router.register('projects', ProjectViewSet)

project_router = routers.NestedSimpleRouter(
    helpdesk_router, 'projects', lookup='projects'
    )
project_router.register('users', ContributorViewSet, basename='user')
project_router.register('issues', IssueViewSet, basename='issue')

issue_router = routers.NestedSimpleRouter(
    project_router, 'issues', lookup='issue'
    )
issue_router.register('comments', ,basename='comment')

urlpatterns = [
    path('', include(helpdesk_router.urls)),
    path('', include(project_router.urls), name='project'),
]
