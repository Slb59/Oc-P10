from django.urls import path, include
from rest_framework import routers

app_name = "helpdesk"

helpdesk_router = routers.SimpleRouter()
# helpdesk_router.register('projects', ?? , basename='projects')

urlpatterns = [
    path('', include(helpdesk_router.urls))
]
