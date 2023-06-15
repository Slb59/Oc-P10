from django.urls import path, include
from rest_framework import routers

app_name = "account"

account_router = routers.SimpleRouter()
# account_router.register('login', ?? )
# account_router.register('signup', ?? )

urlpatterns = [
    path("", include("django.contrib.auth.urls")),
]
