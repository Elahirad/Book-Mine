from rest_framework.serializers import ModelSerializer
from store.models import Category, Product, ProductFile


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'title']


class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'category', 'title', 'description', 'unit_price']


class ProductFileSerializer(ModelSerializer):

    def save(self, **kwargs):
        prodcut_id = self.context['product_id']
        ProductFile.objects.create(product_id=prodcut_id, **self.validated_data)

    class Meta:
        model = ProductFile
        fields = ['id', 'file']
