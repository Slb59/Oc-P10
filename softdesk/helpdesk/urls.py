from django.urls import path, include
from rest_framework_nested import routers

from .views import ProjectViewSet

app_name = "helpdesk"

helpdesk_router = routers.SimpleRouter()
helpdesk_router.register('projects', ProjectViewSet, basename='projects')

urlpatterns = [
    path('', include(helpdesk_router.urls))
]
