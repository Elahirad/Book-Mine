from django.contrib.admin import ModelAdmin
from django.contrib import admin
from django.utils.http import urlencode
from django.utils.html import format_html
from django.urls import reverse
from django.db.models import Count
from . import models


@admin.register(models.Customer)
class CustomerAdmin(ModelAdmin):
    autocomplete_fields = ['user']
    fields = ['user', 'phone']
    list_display = ['user', 'phone', 'email']
    list_per_page = 10

    @admin.display(ordering='user__email')
    def email(self, customer):
        return customer.user.email


@admin.register(models.Category)
class CategoryAdmin(ModelAdmin):
    list_display = ['title', 'added_at', 'products_count']
    list_per_page = 10
    search_fields = ['title']

    def products_count(self, category):
        url = reverse('admin:store_product_changelist')
        return format_html(
            "<a href='{}'>{}</a>",
            url +
            "?" +
            urlencode({
                'category_id': str(category.id)
            }),
            category.products_count
        )

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(products_count=Count('product'))


class ProductFileInline(admin.TabularInline):
    model = models.ProductFile
    min_num = 1
    max_num = 10
    extra = 0


@admin.register(models.Product)
class ProductAdmin(ModelAdmin):
    autocomplete_fields = ['category']
    inlines = [ProductFileInline]
    list_display = ['title', 'unit_price', 'category']


class OrderItemInline(admin.StackedInline):
    model = models.OrderItem
    min_num = 1
    max_num = 10
    extra = 0


@admin.register(models.Order)
class OrderAdmin(ModelAdmin):
    fields = ['customer', 'placed_at', 'order_status']
    inlines = [OrderItemInline]
    list_display = ['customer', 'order_status']
