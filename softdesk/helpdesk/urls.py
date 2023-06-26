from django.urls import path, include
from rest_framework_nested import routers

from .views import ProjectViewSet
# from .views import ContributorViewSet

app_name = "helpdesk"

helpdesk_router = routers.SimpleRouter()
helpdesk_router.register('projects', ProjectViewSet)
helpdesk_router_nested = routers.NestedSimpleRouter(
    helpdesk_router, 'projects', lookup='projects'
    )

urlpatterns = [
    path('', include(helpdesk_router.urls))
]
