from django.contrib.auth.models import AbstractUser
from django.db import models
# from django.contrib.auth.models import User

# Create your models here.

# QUESTION admin panel user creation - password not hashed, authentication does not work
# If I'm creating a user from command line with:
# User.objects.create_user(username='username', email='user5@email.com'  ,password='bar')
# The password in Django is encrypted, but if I'm adding a user from the Django admin panel,
# the password is not encrypted and even the authentication for this user does not work...

class User(AbstractUser):
    email = models.EmailField(unique=True, null=False)
    username = models.CharField(max_length=12, unique=False, null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def profile(self):
        profile = Profile.objects.get(user=self)
        return profile
    
    def __str__(self) -> str:
        return self.email + ", pk: " + str(self.pk)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=False)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    # avatar = models.ImageField(upload_to='images/') # https://codinggear.org/how-to-upload-images-in-django/ # TODO
    # verifiedEmail = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.first_name + " " + self.last_name + ", user pk: " + str(self.user.pk)