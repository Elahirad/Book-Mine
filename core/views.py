from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions
from core.serializers import CreateUserSerializer, UpdateUserSerializer, UserSerializer
from .models import User


class UserViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'patch']

    def get_queryset(self):
        if self.request.user.is_staff:
            return User.objects.all()
        return User.objects.filter(pk=self.request.user.id)

    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateUserSerializer
        elif self.request.method == 'PATCH':
            return UpdateUserSerializer
        return UserSerializer
