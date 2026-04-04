from catalog_app.models import Category, Product, ProductImage
from catalog_app.serializers import CategorySerializer, ProductSerializer, ProductImageSerializer

from rest_framework import permissions
from rest_framework import viewsets

from catalog_app.permissions import IsOwnerOrReadOnly

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

class ProductImageViewSet(viewsets.ModelViewSet):
    queryset = ProductImage.all()
    serializer_class = ProductImageSerializer