from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name',
                  'last_name', 'email', 'is_staff', 'is_active']


class CreateUserSerializer(serializers.ModelSerializer):

    def save(self, **kwargs):
        self.validated_data['password'] = make_password(
            self.validated_data['password'])
        return super().save(**kwargs)

    class Meta:
        model = User
        fields = ['username', 'password', 'first_name',
                  'last_name', 'email']


class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
