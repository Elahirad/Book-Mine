from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework import permissions
from store.models import Category, Product, ProductFile
from store.permissions import IsAdminOrReadOnly
from store.serializers import CategorySerializer, ProductFileSerializer, ProductSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAdminOrReadOnly]


class ProductFileViewSet(viewsets.ModelViewSet):
    queryset = ProductFile.objects.all()
    serializer_class = ProductFileSerializer
    permission_classes = [IsAdminOrReadOnly]

    def create(self, request, *args, **kwargs):
        product_existance_check(self)
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        product_existance_check(self)
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        product_existance_check(self)
        return super().destroy(request, *args, **kwargs)

    def get_object(self):
        product_existance_check(self)
        return super().get_object()

    def get_queryset(self):
        product_existance_check(self)
        product_id = self.kwargs['product_pk']
        return ProductFile.objects.filter(product_id=product_id)

    def get_serializer_context(self):
        product_id = self.kwargs['product_pk']
        return {'product_id': product_id}


def product_existance_check(self):
    product_id = self.kwargs['product_pk']
    get_object_or_404(Product, pk=product_id)
