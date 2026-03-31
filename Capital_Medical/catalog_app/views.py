from django.contrib.auth.models import Group, User
from catalog_app.models import Category

from catalog_app.serializers import CategorySerializer

from django.http import Http404


from rest_framework import generics

class CategoryList(generics.ListCreateAPIView):
    """
    List all categories / create one category
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    
    
class CategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a category instance.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    