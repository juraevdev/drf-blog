from rest_framework import serializers
from blog.models import Category, BlogPost
from django.core.exceptions import ValidationError

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name']

class BlogPostSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    image = serializers.ImageField()

    class Meta:
        model = BlogPost
        fields = ['title', 'description', 'image', 'category', 'author']

    def validate_image(self, value):
        if not value.name.endswith(('.png', '.jpg', '.jpeg')):
            raise ValidationError("Image format must be .png, .jpg, or .jpeg ")
        return value