from urllib import response
from rest_framework import status
from core.models import User
from model_bakery import baker
import pytest


@pytest.fixture
def create_user(api_client):
    def do(user):
        return api_client.post('/auth/users/', user)
    return do


@pytest.fixture
def get_users(api_client):
    def do(id=None):
        if id is None:
            return api_client.get('/auth/users/')
        return api_client.get(f'/auth/users/{id}/')
    return do


@pytest.mark.django_db
class TestCreateUser:
    def test_returns_400_if_invalid(self, create_user):
        response = create_user({'username': ''})

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_returns_200_if_valid(self, create_user):
        response = create_user(
            {
                'username': 'abcdefg',
                'first_name': 'aaaaaa',
                'last_name': 'bbbbbb',
                'password': 'AbCdEfGhI123456789',
                'email': 'aaaa@bbbb.com'
            }
        )

        user = User.objects.get(pk=response.data['id'])

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data == {
            'id': user.id,
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'password': user.password,
            'email': user.email
        }


