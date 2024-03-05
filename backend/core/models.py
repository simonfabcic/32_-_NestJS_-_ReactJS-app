from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Customer(models.Model):
    # https://docs.djangoproject.com/en/5.0/ref/contrib/auth/
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # TODO avatar = 