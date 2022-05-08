from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import LimitOffsetPagination

from .models import (
    Favourite,
    CartShopping,
    Ingredient,
    Recipe,
    Tag
)
from .serializers import (
    IngredientSerializer,
    TagSerializer,
    RecipeSerializer
)
from api.pagination import LimitPageNumberPagination
from api.filters import (
    AuthorRecipeFilter,
    IsFavoritedFilter,
    IsInShoppingCartFilter,
    TagsSlugFilter,
    IngredientSearchFilter
)
from api.permissions import UserOrReadOnly
from users.serializers import RecipeUser

class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = (
        IsFavoritedFilter,
        IsInShoppingCartFilter,
        AuthorRecipeFilter,
        TagsSlugFilter
    )
    filterset_fields = ('is_favorited', 'is_in_shopping_cart',
                        'author', 'tags')
    permission_classes = (IsAuthenticated,)

    @action(
        methods=['post', 'delete'],
        detail=True,
        url_path='favorite',
        permission_classes=(UserOrReadOnly,)
    )
    def favorite(self, request, pk=None):
        user = request.user
        recipe = get_object_or_404(
            Recipe,
            id=self.kwargs.get('pk')
        )
        if request.method == 'POST':
            favorite_recipe = Favourite.objects.create(
                user=user,
                recipe=recipe
            )
            serializer = RecipeUser(
                favorite_recipe.recipe
            )
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        Favourite.objects.filter(
            user=user,
            recipe=recipe
        ).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        methods=['post', 'delete'],
        detail=True,
        url_path='shopping_cart',
        permission_classes=(UserOrReadOnly,)
    )
    def shopping_cart(self, request, pk=None):
        user = request.user
        recipe = get_object_or_404(
            Recipe,
            id=self.kwargs.get('pk')
        )
        if request.method == 'POST':
            cart_recipes = CartShopping.objects.create(
                user=user,
                recipe=recipe
            )
            serializer = RecipeUser(
                cart_recipes.recipe,
            )
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        CartShopping.objects.filter(
            user=user,
            recipe=recipe
        ).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_create(self, serializer):
            serializer.save(author=self.request.user)
