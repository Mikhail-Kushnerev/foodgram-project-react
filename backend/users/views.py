from djoser.views import UserViewSet
from rest_framework import viewsets
from rest_framework import mixins

from .models import User
from .serializers import UserSerializer

class CreateRetrieveViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
):
    pass 

class UserViewset(UserViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    # @action(["get"], detail=False)
    # def me(self, request, *args, **kwargs):
    #     self.get_object = self.get_instance
    #     if request.method == "GET":
    #         return self.retrieve(request, *args, **kwargs)
    # def get_serializer_class(self):
    #     # Если запрошенное действие (action) — получение списка объектов ('list')
    #     if self.action == 'list':
    #         # ...то применяем CatListSerializer
    #         return CustomUserSerializer
    #     # А если запрошенное действие — не 'list', применяем CatSerializer
    #     return UserSerializer 

