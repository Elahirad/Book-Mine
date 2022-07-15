from rest_framework import status
from model_bakery import baker
from store.models import Category, Product
import pytest


@pytest.fixture
def get_products(api_client):
    def do(id=None):
        if id is None:
            return api_client.get('/store/products/')
        return api_client.get(f'/store/products/{id}/')
    return do


@pytest.fixture
def create_product(api_client):
    def do(product):
        return api_client.post('/store/products/', product)
    return do


@pytest.fixture
def update_product_patch(api_client):
    def do(id, product):
        return api_client.patch(f'/store/products/{id}/', product)
    return do


@pytest.fixture
def update_product_put(api_client):
    def do(id, product):
        return api_client.put(f'/store/products/{id}/', product)
    return do


@pytest.fixture
def delete_product(api_client):
    def do(id):
        return api_client.delete(f'/store/products/{id}/')
    return do


@pytest.mark.django_db
class TestRetrieveProduct:
    def test_returns_404_if_does_not_exist(self, get_products):
        response = get_products(1)

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_returns_200_and_product_if_exist(self, get_products):
        category = baker.make(Category)
        product = baker.make(Product, category=category)

        response = get_products(product.id)

        assert response.status_code == status.HTTP_200_OK
        assert response.data == {
            'id': product.id,
            'title': product.title,
            'category': category.id,
            'description': product.description,
            'unit_price': product.unit_price
        }


@pytest.mark.django_db
class TestListProducts:
    def test_returns_200_and_products(self, get_products):
        category = baker.make(Category)
        products = baker.make(Product, 8, category=category)

        response = get_products()

        assert response.status_code == status.HTTP_200_OK
        assert response.data == [
            {
                'id': product.id,
                'title': product.title,
                'category': category.id,
                'description': product.description,
                'unit_price': product.unit_price
            }
            for product in products
        ]


@pytest.mark.django_db
class TestCreateProducts:
    def test_returns_401_if_anonymous(self, create_product):

        response = create_product({'title': 'a'})

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_returns_403_if_not_admin(self, create_product, authorize):
        authorize()

        response = create_product({'title': 'a'})

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_returns_400_if_invalid(self, create_product, authorize):
        authorize(True)

        response = create_product({'title': 'a'})

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_returns_201_if_valid(self, create_product, authorize):
        authorize(True)
        category = baker.make(Category)

        response = create_product({
            'title': 'a',
            'description': 'aa',
            'unit_price': 1,
            'category': category.id
        })
        product = Product.objects.get(pk=response.data['id'])

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data == {
            'id': product.id,
            'title': product.title,
            'description': product.description,
            'unit_price': product.unit_price,
            'category': product.category.id
        }


@pytest.mark.django_db
class TestUpdateProducts:
    def test_returns_401_if_anonymous(self, update_product_patch, update_product_put):

        response = update_product_patch(1, {'title': 'a'})
        response_2 = update_product_put(1, {'title': 'a'})

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response_2.status_code == status.HTTP_401_UNAUTHORIZED

    def test_returns_403_if_not_admin(self, update_product_patch, update_product_put, authorize):
        authorize()

        response = update_product_patch(1, {'title': 'a'})
        response_2 = update_product_put(1, {'title': 'a'})

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert response_2.status_code == status.HTTP_403_FORBIDDEN

    def test_returns_404_if_not_found(self, update_product_patch, update_product_put, authorize):
        authorize(True)

        response = update_product_patch(1, {})
        response_2 = update_product_put(1, {})

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response_2.status_code == status.HTTP_404_NOT_FOUND

    def test_returns_400_if_invalid(self, update_product_patch, update_product_put, authorize):
        authorize(True)
        category = baker.make(Category)
        product = baker.make(Product, category=category)

        response = update_product_patch(product.id, {'unit_price': 'a'})
        response_2 = update_product_put(product.id, {'unit_price': 'a'})

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response_2.status_code == status.HTTP_400_BAD_REQUEST

    def test_returns_200_if_valid(self, update_product_patch, update_product_put, authorize):
        authorize(True)
        category = baker.make(Category)
        product = baker.make(Product, category=category)
        new_product = {
            'title': 'AAA',
            'description': 'AA',
            'unit_price': 4.5,
            'category': category.id
        }

        response = update_product_patch(product.id, new_product)
        response_2 = update_product_put(product.id, new_product)

        assert response.status_code == status.HTTP_200_OK
        assert response.data == {
            'id': product.id,
            'title': new_product['title'],
            'description': new_product['description'],
            'unit_price': new_product['unit_price'],
            'category': new_product['category']
        }
        assert response_2.status_code == status.HTTP_200_OK
        assert response_2.data == {
            'id': product.id,
            'title': new_product['title'],
            'description': new_product['description'],
            'unit_price': new_product['unit_price'],
            'category': new_product['category']
        }


@pytest.mark.django_db
class TestDeleteProducts:
    def test_returns_401_if_anonymous(self, delete_product):

        response = delete_product(1)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_returns_403_if_not_admin(self, delete_product, authorize):
        authorize()

        response = delete_product(1)

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_returns_404_if_not_found(self, delete_product, authorize):
        authorize(True)

        response = delete_product(1)

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_returns_204_if_found(self, delete_product, authorize):
        authorize(True)
        category = baker.make(Category)
        product = baker.make(Product, category=category)

        response = delete_product(product.id)
        count_in_db = Product.objects.filter(pk=product.id).count()

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert count_in_db == 0