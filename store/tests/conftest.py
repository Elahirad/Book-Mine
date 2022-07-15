from rest_framework.test import APIClient
from core.models import User
import pytest


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def authorize(api_client):
    def do(is_staff=False):
        api_client.force_authenticate(user=User(is_staff=is_staff))
    return do
