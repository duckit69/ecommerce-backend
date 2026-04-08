from rest_framework import serializers
from catalog_app.models import Category, Product, ProductImage

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
        read_only_fields=['created_by']


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model=Product
        fields='__all__'
        read_only_fields=['created_by', 'sku', 'created_at', 'updated_at']
    

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model=ProductImage
        fields='__all__'
        read_only_fields=['created_at']