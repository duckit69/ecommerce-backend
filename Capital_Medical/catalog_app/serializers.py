from rest_framework import serializers
from catalog_app.models import Category

class CategorySerializer(serializers.HyperlinkedModelSerializer):
    manager = serializers.HyperlinkedRelatedField(
        view_name='user-detail',
        read_only=True
    )
    class Meta:
        model = Category
        fields = '__all__'