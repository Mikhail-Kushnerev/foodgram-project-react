from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from recipes.models import (AmountOfIngrediend, CartShopping, Favourite,
                            Ingredient, Recipe, Tag)
from users.serializers import RecipeUser

from .filters import IngredientFilter, UserRecipeFilter
from .pagination import PageNumberPagination
from .permissions import IsAdminOrReadOnly, IsAuthorOrReadOnly
from .serializers import IngredientSerializer, RecipeSerializer, TagSerializer
from .utils import download_page


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (IsAdminOrReadOnly,)


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_class = IngredientFilter
    permission_classes = (IsAdminOrReadOnly,)


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    pagination_class = PageNumberPagination
    filter_class = UserRecipeFilter
    permission_classes = (IsAuthorOrReadOnly,)

    @action(
        methods=['post', 'delete'],
        detail=True,
        url_path='favorite',
        permission_classes=(IsAuthenticated,)
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
        permission_classes=(IsAuthenticated,)
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

    @action(
        detail=False,
        url_path='download_shopping_cart',
        permission_classes=(IsAuthenticated,)
    )
    def download_shopping_cart(self, request):
        unit_sum_dict = {}
        user = request.user
        cart_list = AmountOfIngrediend.objects.filter(
            recipe__cart_shoppings__user=user
        ).values_list(
            'ingredient__name',
            'ingredient__measurement_unit',
            'amount'
        )
        for item in cart_list:
            name = item[0]
            if name not in unit_sum_dict:
                unit_sum_dict[name] = {
                    'measurement_unit': item[1],
                    'amount': item[2]
                }
            else:
                unit_sum_dict[name]['amount'] += item[2]
        return download_page(unit_sum_dict)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
