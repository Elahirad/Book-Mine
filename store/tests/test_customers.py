from rest_framework import status
import pytest


@pytest.fixture
def get_customers(api_client):
    def do(id=None):
        if id == None:
            return api_client.get('/store/customers/')
        return api_client.get(f'/store/customers/{id}/')
    return do


@pytest.mark.django_db
class TestRetrieveCustomers:

    def test_returns_404_if_not_found(self, get_customers):
        response = get_customers(2)

        assert response.status_code == status.HTTP_404_NOT_FOUND
