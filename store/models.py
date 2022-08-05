from django.db import models
from django.conf import settings


class Customer(models.Model):
    phone = models.CharField(max_length=255)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return str(self.user)


class Category(models.Model):
    class Meta:
        verbose_name_plural = 'categories'

    title = models.CharField(max_length=255)
    added_at = models.DateField(auto_now_add=True)

    def __str__(self) -> str:
        return str(self.title)


class Product(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)
    added_at = models.DateField(auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return str(self.title)


class ProductFile(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='files')
    file = models.FileField(upload_to='store/products/files')


class Order(models.Model):
    PENDING_ORDER = 'P'
    COMPLETED_ORDER = 'C'
    CANCELED_ORDER = 'A'
    ORDER_STATUS_CHOICES = [
        (PENDING_ORDER, 'Pending'),
        (COMPLETED_ORDER, 'Completed'),
        (CANCELED_ORDER, 'Canceled')
    ]
    placed_at = models.DateTimeField(auto_now_add=True)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)
    order_status = models.CharField(max_length=1, choices=ORDER_STATUS_CHOICES)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.IntegerField()
