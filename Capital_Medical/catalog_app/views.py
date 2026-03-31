from catalog_app.models import Category
from catalog_app.serializers import CategorySerializer

from rest_framework import generics
from rest_framework import permissions

from catalog_app.permissions import IsOwnerOrReadOnly
class CategoryList(generics.ListCreateAPIView):
    """
    GET all categories / POST category
    
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def perform_create(self, serializer):
        serializer.save(manager=self.request.user)
    
    
class CategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    GET 1, PUT(all fields must be present) or DELETE a category instance.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    