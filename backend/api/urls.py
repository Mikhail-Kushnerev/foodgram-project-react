from django.urls import path, include
from rest_framework.routers import DefaultRouter

from users.views import UserViewset

router = DefaultRouter()
router.register('users', UserViewset, basename='users')


urlpatterns = [
    path('', include(router.urls)),
    # path('', include('djoser.urls')),
    # path('', include(router.urls)),
    path('auth/', include('djoser.urls.authtoken')),
]