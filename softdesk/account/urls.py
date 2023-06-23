from django.urls import path, include
from rest_framework_nested import routers
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView

from .views import UserViewSet

app_name = "account"

account_router = routers.DefaultRouter()
# account_router.register('login', ?? )
account_router.register('signup', UserViewSet)

urlpatterns = [
    path('', include(account_router.urls)),
    # path('signup/', UserViewSet.as_view(), name='signup'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path(
        'login/refreshtoken/', TokenRefreshView.as_view(), name='token_refresh'
        ),
    # path('api-auth/', include('rest_framework.urls'))
]
