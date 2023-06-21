"""
URL configuration for softdesk project.
"""

from django.contrib import admin
from django.urls import path, include
from rest_framework.schemas import get_schema_view

schema_view = get_schema_view(title='SoftDesk API')

urlpatterns = [
    path("admin/", admin.site.urls),
    path("users/", include("softdesk.account.urls")),
    path("", include("softdesk.helpdesk.urls")),
    path('schema/', schema_view),
]
