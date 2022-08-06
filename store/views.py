from uuid import uuid4
from django.shortcuts import get_object_or_404
from django.http import FileResponse
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework import mixins
from rest_framework.response import Response
from rest_framework import status
from store.models import Category, Customer, Order, Product, ProductFile
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


class ProductFileViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
):

    http_method_names = ['get']
    serializer_class = ProductFileSerializer

    def get_serializer_context(self):
        return {'request': self.request}

    def get_queryset(self):
        product_id = self.kwargs['product_pk']
        return ProductFile.objects.filter(product_id=product_id)

    def list(self, request, *args, **kwargs):
        (orders, product_id) = prepere_files(self)

        for order in orders:
            if order.items.filter(product_id=product_id).count() > 0:
                return super().list(request)

        return Response(
            {
                'message': "You don't have this product in your owned products."
            },
            status=status.HTTP_403_FORBIDDEN
        )

    def retrieve(self, request, *args, **kwargs):
        (orders, product_id) = prepere_files(self)

        for order in orders:
            if order.items.filter(product_id=product_id).count() > 0:
                instance = self.get_object()
                file_handle = instance.file.open()

                response = FileResponse(
                    file_handle, content_type='application/pdf')
                response['Content-Length'] = instance.file.size
                response['Content-Disposition'] = f'attachment; filename="{uuid4()}.pdf"'
                return response

        return Response(
            {
                'message': "You don't have this product in your owned products."
            },
            status=status.HTTP_403_FORBIDDEN
        )


def prepere_files(self):
    product_id = self.kwargs['product_pk']
    get_object_or_404(Product, pk=product_id)
    user = self.request.user
    customer = Customer.objects.get(user=user)
    return (Order.objects.filter(customer_id=customer.id, order_status='C'), product_id)
