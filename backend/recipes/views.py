from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from rest_framework import (
    status,
    viewsets
)
from rest_framework.decorators import action
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from users.serializers import RecipeUser
from api.filters import (
    IngredientFilter,
    UserRecipeFilter
)
from api.pagination import LimitPageNumberPagination
from api.permissions import (
    IsOwnerOrReadOnly,
    IsAdminOrReadOnly
)
from .models import (
    AmountOfIngrediend,
    CartShopping,
    Favourite,
    Ingredient,
    Recipe,
    Tag
)
from .serializers import (
    IngredientSerializer,
    RecipeSerializer,
    TagSerializer
)


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
    pagination_class = LimitOffsetPagination
    filter_class = UserRecipeFilter
    permission_classes = [IsOwnerOrReadOnly]

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
        url_path='download_shopping_cart'
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
            unit_sum_dict[item[0]] = {
                'ед. изм.': item[1],
                'кол-во': item[2],
            }
        response = HttpResponse(
            unit_sum_dict,
            content_type='application/txt'
        )
        response['Content-Disposition'] = (
            'attachment; '
            'filename="cart_list.txt"'
        )
        response.write(u'\ufeff'.encode('utf8'))
        return response
        # writer = csv.writer(response, delimiter=';')
    def perform_create(self, serializer):
            serializer.save(author=self.request.user)
