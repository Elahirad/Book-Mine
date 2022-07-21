from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework import permissions
from store.models import Category, Customer, Product, ProductFile
from store.permissions import IsAdminOrReadOnly
from store.serializers import CategorySerializer, CustomerSerializer, ProductFileSerializer, ProductSerializer, UpdateCustomerSerializer


class CustomerViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'patch', 'options', 'head']
    serializer_class = CustomerSerializer

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return [permissions.IsAuthenticated()]
        return [permissions.IsAdminUser()]

    def get_serializer_class(self):
        if self.request.method == 'patch':
            return UpdateCustomerSerializer
        return CustomerSerializer

    def get_queryset(self):
        if self.request.user.is_staff:
            return Customer.objects.all()
        return Customer.objects.filter(user_id=self.request.user.id)


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
