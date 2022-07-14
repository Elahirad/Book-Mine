from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers
from . import views

router = DefaultRouter()
router.register('categories', views.CategoryViewSet, basename='categories')
router.register('products', views.ProductViewSet, basename='products')


product_router = routers.NestedDefaultRouter(
    router, 'products', lookup='product')
product_router.register(
    'files', views.ProductFileViewSet, basename='product-files')


urlpatterns = router.urls + product_router.urls
