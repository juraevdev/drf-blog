from django.urls import path
from blog.views import (
    CategoryListApiView,
    CategoryCreateApiView,
    CategoryDetailApiView,
    BlogPostListApiView,
    BlogPostCreateApiView,
    BlogPostDetailApiView,
)

urlpatterns = [
    path('category/', CategoryListApiView.as_view()),
    path('category/new/', CategoryCreateApiView.as_view()),
    path('category/<int:id>/', CategoryDetailApiView.as_view()),
    path('blogpost/', BlogPostListApiView.as_view()),
    path('blogpost/new/', BlogPostCreateApiView.as_view()),
    path('blogpost/<int:id>/', BlogPostDetailApiView.as_view()),
]