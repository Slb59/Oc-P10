from django.urls import path, include
from rest_framework_nested import routers

from .views_project import ProjectViewSet
from .views_project import ContributorViewSet
from .views_issue import IssueViewSet
from .views_comment import CommentViewSet

app_name = "helpdesk"

# add project endpoint
helpdesk_router = routers.SimpleRouter()
helpdesk_router.register('projects', ProjectViewSet)

# add users and issues endpoint
project_router = routers.NestedSimpleRouter(
    helpdesk_router, 'projects', lookup='projects'
    )
project_router.register('users', ContributorViewSet, basename='user')
project_router.register('issues', IssueViewSet, basename='issue')

# add comments end point
issue_router = routers.NestedSimpleRouter(
    project_router, 'issues', lookup='issue'
    )
issue_router.register('comments', CommentViewSet, basename='comment')

urlpatterns = [
    path('', include(helpdesk_router.urls)),
    path('', include(project_router.urls), name='project'),
]
