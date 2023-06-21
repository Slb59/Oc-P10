"""
URL configuration for softdesk project.
"""

from django.contrib import admin
from django.urls import path, include
from rest_framework.documentation import include_docs_urls
from rest_framework.schemas import get_schema_view

API_TITLE = 'SoftDesk API'
API_DESCRIPTION = 'A Web API for tracking issue on projects'

schema_view = get_schema_view(title=API_TITLE)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("softdesk.account.urls")),
    path("projects/", include("softdesk.helpdesk.urls")),
    path('schema/', schema_view),
    path('docs/', include_docs_urls(
        title=API_TITLE,
        description=API_DESCRIPTION
        )),
]
