from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class User(AbstractUser):
    email = models.EmailField(unique=True, null=False)
    username = models.CharField(max_length=12, unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def profile(self):
        profile = Profile.objects.get(user=self)
        return profile
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=False)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    # avatar = models.ImageField(upload_to='images/') # https://codinggear.org/how-to-upload-images-in-django/
    # verifiedEmail = models.BooleanField(default=False)

# # This stuff works:
# class Role(models.Model):
#     name=models.CharField(max_length=20)

# class Customer(models.Model): # member
#     # https://docs.djangoproject.com/en/5.0/ref/contrib/auth/
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     # TODO avatar = 