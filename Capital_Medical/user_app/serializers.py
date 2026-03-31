from django.contrib.auth.models import User

from rest_framework import serializers


#import Category Model
from catalog_app.models import Category

class UserSerializer(serializers.ModelSerializer):
    categories = serializers.PrimaryKeyRelatedField(
        many = True,
        queryset = Category.objects.all()
    )
    
    class Meta:
        model = User
        fields = ['id', 'username', 'categories']