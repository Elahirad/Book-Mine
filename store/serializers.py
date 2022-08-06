from rest_framework.serializers import ModelSerializer, SerializerMethodField
from store.models import Category, Customer, Product, ProductFile
import os


class UpdateCustomerSerializer(ModelSerializer):
    class Meta:
        model = Customer
        fields = ['phone']


class CustomerSerializer(ModelSerializer):
    username = SerializerMethodField('get_username')
    first_name = SerializerMethodField('get_first_name')
    last_name = SerializerMethodField('get_last_name')
    email = SerializerMethodField('get_email')

    def get_username(self, customer):
        return customer.user.username

    def get_first_name(self, customer):
        return customer.user.first_name

    def get_last_name(self, customer):
        return customer.user.last_name

    def get_email(self, customer):
        return customer.user.email

    class Meta:
        model = Customer
        fields = ['id', 'username', 'first_name',
                  'last_name', 'email', 'phone']


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'title']


class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'category', 'title', 'description', 'unit_price']


class ProductFileSerializer(ModelSerializer):

    filename = SerializerMethodField('get_filename')

    url = SerializerMethodField('get_url')

    def save(self, **kwargs):
        prodcut_id = self.context['product_id']
        ProductFile.objects.create(
            product_id=prodcut_id, **self.validated_data)

    def get_filename(self, productfile):
        return os.path.basename(productfile.file.name)

    def get_url(self, productfile):
        request = self.context['request']
        return request.build_absolute_uri(
            f'/store/products/{productfile.product.id}/files/{productfile.id}/'
        )

    class Meta:
        model = ProductFile
        fields = ['id', 'filename', 'url']
