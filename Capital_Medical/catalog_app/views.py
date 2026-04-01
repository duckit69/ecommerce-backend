from catalog_app.models import Category
from catalog_app.serializers import CategorySerializer

from rest_framework import permissions
from rest_framework import viewsets

from catalog_app.permissions import IsOwnerOrReadOnly

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    
    def perform_create(self, serializer):
        serializer.save(manager=self.request.user)

