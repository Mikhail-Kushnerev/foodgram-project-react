from rest_framework import serializers

from .models import User

class Login_Serializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'password')