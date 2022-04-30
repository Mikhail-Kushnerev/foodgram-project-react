from rest_framework import viewsets
from rest_framework.decorators import api_view

from .models import User
from .serializers import Login_Serializer

@api_view(['POST'])
class Login(viewsets.ModelViewSet):
    
    serializer_classes = Login_Serializer

    def get_queryset(self):
        return User.objects.get(user=self.request.email).auth_token