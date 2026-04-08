from django.urls import path, include
from rest_framework.routers import DefaultRouter

from catalog_app import views

router = DefaultRouter()

router.register(r'categories', views.CategoryViewSet, basename='category')
router.register(r'products', views.ProductViewSet, basename='product')
router.register(r'productImage', views.ProductImageViewSet, basename='productImage')

urlpatterns = [
    path("", include(router.urls)),
]
