from django.urls import path, include
from rest_framework_nested import routers

from .views.views_project import ProjectViewSet
from .views.views_project import ContributorViewSet
from .views.views_issue import IssueViewSet
from .views.views_comment import CommentViewSet

app_name = "helpdesk"

# add project endpoint
helpdesk_router = routers.SimpleRouter()
helpdesk_router.register('projects', ProjectViewSet)

# add users and issues endpoint
project_router = routers.NestedSimpleRouter(
    helpdesk_router, 'projects', lookup='projects'
    )
project_router.register('users', ContributorViewSet, basename='users')
project_router.register('issues', IssueViewSet, basename='issues')

# add comments end point
issue_router = routers.NestedSimpleRouter(
    project_router, 'issues', lookup='issues'
    )
issue_router.register('comments', CommentViewSet, basename='comments')

urlpatterns = [
    path('', include(helpdesk_router.urls)),
    path('', include(project_router.urls), name='projects'),
    path('', include(issue_router.urls), name='issues'),
]
