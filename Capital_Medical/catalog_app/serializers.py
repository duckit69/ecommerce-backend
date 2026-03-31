from rest_framework import serializers
from catalog_app.models import Category

class CategorySerializer(serializers.ModelSerializer):
    manager = serializers.ReadOnlyField(source='manager.username')
    class Meta:
        model = Category
        fields = '__all__'