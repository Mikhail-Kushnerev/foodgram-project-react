from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Subscription, User
from .serializers import CustomUserSerializer


class UserViewset(UserViewSet):
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    pagination_class = LimitOffsetPagination
 
    
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
            serializer = self.get_serializer(subscription.author)
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
    )
    def subscriptions(self, request):
        user = request.user
        user = get_object_or_404( 
            User, 
            id=user.id
        )
        queryset = [i.author for i in user.follower.all()]
        page = self.paginate_queryset(queryset)
        if page:
            serializer = self.get_serializer(
                page,
                many=True
            )
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(
            queryset,
            many=True
        )
        return  Response(
            serializer.data,
            status=status.HTTP_200_OK
        )
