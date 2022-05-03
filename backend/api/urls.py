from django.urls import path, include
from rest_framework.routers import DefaultRouter

from recipes.views import TagViewSet
from users.views import (
    UserViewset
)

router = DefaultRouter()
router.register('tags', TagViewSet, basename="tags")
router.register('users', UserViewset)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('djoser.urls.authtoken')),
]