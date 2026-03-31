from django.contrib.auth.models import User

from rest_framework import serializers


#import Category Model
from catalog_app.models import Category

class UserSerializer(serializers.ModelSerializer):
    managed_categories = serializers.PrimaryKeyRelatedField(
        many = True,
        queryset = Category.objects.all()
    )
    
    class Meta:
        model = User
        fields = ['id', 'username', 'managed_categories']