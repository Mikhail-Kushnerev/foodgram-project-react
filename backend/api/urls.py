from django.urls import include, path
from recipes.views import (
    IngredientViewSet,
    RecipeViewSet,
    TagViewSet
)
from rest_framework.routers import DefaultRouter
from users.views import UserViewset

router = DefaultRouter()
router.register('users', UserViewset)
router.register('tags', TagViewSet)
router.register('ingredients', IngredientViewSet)
router.register('recipes', RecipeViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('djoser.urls.authtoken')),
]