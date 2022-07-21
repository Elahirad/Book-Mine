from rest_framework import status
from django.conf import settings
from model_bakery import baker
from store.models import Customer
import pytest


@pytest.fixture
def get_customers(api_client):
    def do(id=None):
        if id == None:
            return api_client.get('/store/customers/')
        return api_client.get(f'/store/customers/{id}/')
    return do


@pytest.fixture
def update_customer(api_client):
    def do(id, customer):
        return api_client.patch(f'/store/customers/{id}/', customer)
    return do


@pytest.mark.django_db
class TestRetrieveCustomers:

    def test_returns_401_if_anonymous(self, get_customers):
        response = get_customers(2)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_returns_404_if_not_found(self, get_customers, authorize):
        authorize()

        response = get_customers(2)

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_returns_200(self, get_customers, api_client):
        user = baker.make(settings.AUTH_USER_MODEL)
        api_client.force_authenticate(user=user)
        response = get_customers(user.customer.id)

        assert response.status_code == status.HTTP_200_OK
        assert response.data == {
            'id': user.id,
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'phone': user.customer.phone
        }


@pytest.mark.django_db
class TestListCustomers:
    def test_returns_401_if_anonymous(self, get_customers):
        response = get_customers()

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_returns_200_and_current_customer_if_not_admin(self, api_client, get_customers):
        user = baker.make(settings.AUTH_USER_MODEL)
        users = baker.make(settings.AUTH_USER_MODEL, 12)
        api_client.force_authenticate(user)

        response = get_customers()

        assert response.status_code == status.HTTP_200_OK
        assert response.data == [
            {
                'id': user.id,
                'username': user.username,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
                'phone': user.customer.phone
            }
        ]

    def test_returns_all_customers(self, api_client, get_customers):
        users = baker.make(settings.AUTH_USER_MODEL, 12, is_staff=True)
        api_client.force_authenticate(users[0])

        response = get_customers()

        assert response.status_code == status.HTTP_200_OK
        assert response.data == [
            {
                'id': user.id,
                'username': user.username,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
                'phone': user.customer.phone
            }
            for user in users
        ]


class TestCreateCustomers:

    def test_returns_401_if_anonymous(self, api_client):
        response = api_client.post('/store/customers/', {})

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_returns_403_if_not_admin(self, api_client, authorize):
        authorize()

        response = api_client.post('/store/customers/', {})

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_returns_405(self, api_client, authorize):
        authorize(True)

        response = api_client.post('/store/customers/', {})

        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


@pytest.mark.django_db
class TestUpdateCustomers:
    def test_returns_401_if_anonymous(self, update_customer):

        response = update_customer(1, {})

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_returns_403_if_not_admin(self, authorize, update_customer):
        authorize()

        response = update_customer(1, {})

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_returns_404_if_not_found(self, authorize, update_customer):
        authorize(True)

        response = update_customer(1, {})

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_returns_400_if_invalid(self, api_client, update_customer):
        user = baker.make(settings.AUTH_USER_MODEL, is_staff=True)
        api_client.force_authenticate(user=user)

        response = update_customer(user.customer.id, {'phone': ''})

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_returns_200_if_valid(self, api_client, update_customer):
        user = baker.make(settings.AUTH_USER_MODEL, is_staff=True)
        api_client.force_authenticate(user=user)

        response = update_customer(user.customer.id, {'phone': '123456'})

        assert response.status_code == status.HTTP_200_OK

        assert response.data == {
            'id': user.id,
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'phone': '123456'
        }


@pytest.mark.django_db
class TestDeleteCustomers:
    def test_returns_401_if_anonymous(self, api_client):

        response = api_client.delete('/store/customers/1/')

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_returns_403_if_not_admin(self, authorize, api_client):
        authorize()

        response = response = api_client.delete('/store/customers/1/')

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_returns_405(self, authorize, api_client):
        authorize(True)

        response = response = api_client.delete('/store/customers/1/')

        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
