from rest_framework import status
from model_bakery import baker
from store.models import Category
import pytest


@pytest.fixture
def get_categories(api_client):
    def do(id=None):
        if id is None:
            return api_client.get('/store/categories/')
        return api_client.get(f'/store/categories/{id}/')
    return do


@pytest.fixture
def create_category(api_client):
    def do(category):
        return api_client.post('/store/categories/', category)
    return do


@pytest.fixture
def update_category_patch(api_client):
    def do(id, category):
        return api_client.patch(f'/store/categories/{id}/', category)
    return do


@pytest.fixture
def update_category_put(api_client):
    def do(id, category):
        return api_client.put(f'/store/categories/{id}/', category)
    return do


@pytest.fixture
def delete_category(api_client):
    def do(id):
        return api_client.delete(f'/store/categories/{id}/')
    return do


@pytest.mark.django_db
class TestRetrieveCategory:
    def test_returns_404_if_does_not_exist(self, get_categories):
        response = get_categories(1)

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_returns_200_and_category_if_exist(self, get_categories):
        category = baker.make(Category)

        response = get_categories(category.id)

        assert response.status_code == status.HTTP_200_OK
        assert response.data == {
            'id': category.id,
            'title': category.title,
        }


@pytest.mark.django_db
class TestListCategories:
    def test_returns_200_and_categories(self, get_categories):
        categories = baker.make(Category, 8)

        response = get_categories()

        assert response.status_code == status.HTTP_200_OK
        assert response.data == [
            {
                'id': category.id,
                'title': category.title
            }
            for category in categories
        ]


@pytest.mark.django_db
class TestCreateCategories:
    def test_returns_401_if_anonymous(self, create_category):

        response = create_category({'title': 'a'})

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_returns_403_if_not_admin(self, create_category, authorize):
        authorize()

        response = create_category({'title': 'a'})

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_returns_400_if_invalid(self, create_category, authorize):
        authorize(True)

        response = create_category({'title': ''})

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_returns_201_if_valid(self, create_category, authorize):
        authorize(True)
        category = baker.make(Category)

        response = create_category({
            'title': 'a',
        })
        category = Category.objects.get(pk=response.data['id'])

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data == {
            'id': category.id,
            'title': category.title,
        }


@pytest.mark.django_db
class TestUpdateCategories:
    def test_returns_401_if_anonymous(self, update_category_patch, update_category_put):

        response = update_category_patch(1, {'title': 'a'})
        response_2 = update_category_put(1, {'title': 'a'})

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response_2.status_code == status.HTTP_401_UNAUTHORIZED

    def test_returns_403_if_not_admin(self, update_category_patch, update_category_put, authorize):
        authorize()

        response = update_category_patch(1, {'title': 'a'})
        response_2 = update_category_put(1, {'title': 'a'})

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert response_2.status_code == status.HTTP_403_FORBIDDEN

    def test_returns_404_if_not_found(self, update_category_patch, update_category_put, authorize):
        authorize(True)

        response = update_category_patch(1, {})
        response_2 = update_category_put(1, {})

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response_2.status_code == status.HTTP_404_NOT_FOUND

    def test_returns_400_if_invalid(self, update_category_patch, update_category_put, authorize):
        authorize(True)
        category = baker.make(Category)

        response = update_category_patch(category.id, {'title': ''})
        response_2 = update_category_put(category.id, {'title': ''})

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response_2.status_code == status.HTTP_400_BAD_REQUEST

    def test_returns_200_if_valid(self, update_category_patch, update_category_put, authorize):
        authorize(True)
        category = baker.make(Category)
        new_category = {
            'title': 'AAA',
        }

        response = update_category_patch(category.id, new_category)
        response_2 = update_category_put(category.id, new_category)

        assert response.status_code == status.HTTP_200_OK
        assert response.data == {
            'id': category.id,
            'title': new_category['title'],
        }
        assert response_2.status_code == status.HTTP_200_OK
        assert response_2.data == {
            'id': category.id,
            'title': new_category['title'],
        }


@pytest.mark.django_db
class TestDeleteCategories:
    def test_returns_401_if_anonymous(self, delete_category):

        response = delete_category(1)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_returns_403_if_not_admin(self, delete_category, authorize):
        authorize()

        response = delete_category(1)

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_returns_404_if_not_found(self, delete_category, authorize):
        authorize(True)

        response = delete_category(1)

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_returns_204_if_found(self, delete_category, authorize):
        authorize(True)
        category = baker.make(Category)

        response = delete_category(category.id)
        count_in_db = Category.objects.filter(pk=category.id).count()

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert count_in_db == 0
