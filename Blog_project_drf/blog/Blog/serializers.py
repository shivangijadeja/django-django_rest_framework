from rest_framework import serializers
from .models import Category, Blogs

class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model=Category
        fields='__all__'

class BlogSerializer(serializers.ModelSerializer):

    class Meta:
        model=Blogs
        fields='__all__'