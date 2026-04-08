from django.contrib.auth.models import User

from rest_framework import serializers

class UserSerializer(serializers.HyperlinkedModelSerializer):
    managed_categories = serializers.HyperlinkedRelatedField(
        many = True,
        view_name = 'category-detail',
        read_only = True
    )
    
    class Meta:
        model = User
        fields = ['url', 'id', 'username', 'managed_categories']