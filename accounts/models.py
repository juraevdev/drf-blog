import random, datetime
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from accounts.managers import CustomUserManager

# Create your models here.
class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, unique=True)
    objects = CustomUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    def generate_verify_code(self, request):
        code = ''.join(random.choices('0123456789', k=5))
        user = UserConfirmation.objects.create(
            code = code,
            user = self,
            expires = timezone.now() + datetime.timedelta(minutes=2)
        )
        return code

class UserConfirmation(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='codes')
    code = models.CharField(max_length=5)
    expires = models.DateTimeField(null=True, blank=True)
    is_used = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user} - {self.code}"
    
class PasswordReset(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='passwords')
    code = models.CharField(max_length=5)
    expires = models.DateTimeField(null=True, blank=True)
    is_used = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user} - {self.code}"