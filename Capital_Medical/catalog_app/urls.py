from django.urls import path, include
from rest_framework.routers import DefaultRouter

from catalog_app import views

router = DefaultRouter()

router.register(r'', views.CategoryViewSet, basename='category')

urlpatterns = [
    path("", include(router.urls)),
]
