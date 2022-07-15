from rest_framework.viewsets import ModelViewSet
from core.serializers import CreateUserSerializer, UpdateUserSerializer, UserSerializer
from .models import User


class UserViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'patch']
    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'POSR':
            return CreateUserSerializer
        elif self.request.method == 'PATCH':
            return UpdateUserSerializer
        return UserSerializer
