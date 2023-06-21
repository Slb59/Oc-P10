"""
URL configuration for softdesk project.
"""

from django.contrib import admin
from django.urls import path, include
# from rest_framework.documentation import include_docs_urls
from rest_framework import permissions
# from rest_framework.schemas import get_schema_view
# from rest_framework_swagger.views import get_swagger_view
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

API_TITLE = 'SoftDesk API'
API_DESCRIPTION = 'A Web API for tracking issue on projects'

schema_view = get_schema_view(
    openapi.Info(title=API_TITLE,
                 description=API_DESCRIPTION,
                 default_version='v1'),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("softdesk.account.urls")),
    path("projects/", include("softdesk.helpdesk.urls")),
    path(
        'schema/', schema_view.with_ui('swagger', cache_timeout=0),
        name='schema-swagger-ui'
        ),
    path('docs/', schema_view.with_ui('redoc', cache_timeout=0),
         name='schema-redoc'),
    # path('docs/', include_docs_urls(
    #     title=API_TITLE,
    #     description=API_DESCRIPTION
    #     )),
]
