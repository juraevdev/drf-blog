from django.shortcuts import render
from rest_framework import generics, filters
from blog.serializers import CategorySerializer, BlogPostSerializer
from blog.models import Category, BlogPost

# Create your views here.
class CategoryListApiView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    
class CategoryCreateApiView(generics.CreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class CategoryDetailApiView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CategorySerializer
    lookup_field = 'id'

    def get_queryset(self):
        return Category.objects.all()

class BlogPostListApiView(generics.ListAPIView):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['created_at']
    ordering = ['-created_at']

class BlogPostCreateApiView(generics.CreateAPIView):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer

class BlogPostDetailApiView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = BlogPostSerializer
    lookup_field = 'id'

    def get_queryset(self):
        return BlogPost.objects.all()