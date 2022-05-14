from django.db.models import Sum
from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from recipes.models import (AmountOfIngrediend, CartShopping, Favourite,
                            Ingredient, Recipe, Tag)
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from users.models import Subscription, User

from .filters import IngredientFilter, UserRecipeFilter
from .pagination import PageNumberPagination
from .permissions import IsAdminOrReadOnly, IsAuthorOrReadOnly
from .serializers import (CustomUserSerializer, IngredientSerializer,
                          RecipeSerializer, RecipeSerializerGet,
                          SubscriptionsSerializer, TagSerializer)
from .utils import add_or_delete, download_page


class UserViewset(UserViewSet):
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    pagination_class = PageNumberPagination

    @action(
        methods=['post', 'delete'],
        detail=True,
        url_path='subscribe',
        permission_classes=(IsAuthenticated,),
    )
    def subscribe(self, request, id=None):
        user = request.user
        author = get_object_or_404(
            User,
            id=self.kwargs.get('id')
        )
        if request.method == 'POST':
            subscription = Subscription.objects.create(
                user=user,
                author=author
            )
            serializer = SubscriptionsSerializer(
                subscription.author,
                context={'request': request}
            )
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        Subscription.objects.filter(
            user=user,
            author=author
        ).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=False,
        url_path='subscriptions',
        permission_classes=(IsAuthenticated,),
    )
    def subscriptions(self, request):
        user = request.user
        user = get_object_or_404(
            User,
            id=user.id
        )
        queryset = [i.author for i in user.follower.all()]
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = SubscriptionsSerializer(
                page,
                many=True,
                context={'request': request},
            )
            return self.get_paginated_response(serializer.data)
        serializer = SubscriptionsSerializer(
            queryset,
            many=True,
            context={'request': request},
        )
        return Response(
            serializer.data,
            status=status.HTTP_200_OK
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
    pagination_class = PageNumberPagination
    filter_class = UserRecipeFilter
    permission_classes = (IsAuthorOrReadOnly,)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return RecipeSerializerGet
        return RecipeSerializer

    @action(
        methods=['post', 'delete'],
        detail=True,
        url_path='favorite',
        permission_classes=(IsAuthenticated,)
    )
    def favorite(self, request, pk=None):
        return add_or_delete(request, Favourite, pk)

    @action(
        methods=['post', 'delete'],
        detail=True,
        url_path='shopping_cart',
        permission_classes=(IsAuthenticated,)
    )
    def shopping_cart(self, request, pk=None):
        return add_or_delete(request, CartShopping, pk)

    @action(
        detail=False,
        url_path='download_shopping_cart',
        permission_classes=(IsAuthenticated,)
    )
    def download_shopping_cart(self, request):
        user = request.user
        cart_list = AmountOfIngrediend.objects.filter(
            recipe__cart_shoppings__user=user
        ).values(
            'ingredient__name',
            'ingredient__measurement_unit'
        ).annotate(amount=Sum('amount'))
        # for item in cart_list:
        #     name = item[0]
        #     if name not in unit_sum_dict:
        #         unit_sum_dict[name] = {
        #             'measurement_unit': item[1],
        #             'amount': item[2]
        #         }
        #     else:
        #         unit_sum_dict[name]['amount'] += item[2]
        return download_page(cart_list)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
