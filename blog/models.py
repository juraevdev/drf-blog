from django.db import models
from accounts.models import CustomUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.text import slugify

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=250, unique=True)
    slug = models.SlugField(max_length=250, unique=True)

    def __str__(self):
        return self.name
    
@receiver(post_save, sender=Category)
def category_post_save_slug(sender, instance, created, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.name)
        instance.save()

class BlogPost(models.Model):
    title = models.CharField(max_length=250)
    description = models.TextField(null=True, blank=True)
    slug = models.SlugField(max_length=250, unique=True)
    image = models.ImageField(upload_to='images/%Y/%m/%d/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='blog_posts')
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='posts'
    )

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} - {self.author.first_name}"
    
@receiver(post_save, sender=BlogPost)
def blog_post_slug(sender, instance, created, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.title)
        instance.save()
