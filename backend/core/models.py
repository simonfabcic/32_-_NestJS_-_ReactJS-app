from django.contrib.auth.models import AbstractUser
from django.db import models

# from django.contrib.auth.models import User

# Create your models here.

# QUESTION admin panel user creation - password not hashed, authentication does not work
# If I'm creating a user from command line with:
# User.objects.create_user(username='username', email='user5@example.com'  ,password='bar')
# The password in Django is encrypted, but if I'm adding a user from the Django admin panel,
# the password is not encrypted and even the authentication for this user does not work...


class CoreUser(AbstractUser):
    # JURE I have to inherit from AbstractUser, because of error:
    # Local field 'email' in class 'CoreUser' clashes with field of the same name from base class 'User'.
    email = models.EmailField(unique=True, null=False)
    # username = models.CharField(max_length=12, unique=False, null=True, blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]
    # JURE I have to put the line above back, because of error:
    # core.CoreUser: (auth.E002) The field named as the 'USERNAME_FIELD' for a custom user model must not be included in 'REQUIRED_FIELDS'.
    # HINT: The 'USERNAME_FIELD' is currently set to 'email', you should remove 'email' from the 'REQUIRED_FIELDS'.

    # def profile(self):
    #     profile = Profile.objects.get(user=self)
    #     return profile

    def __str__(self) -> str:
        return self.email + ", pk: " + str(self.pk)


class CoreProfile(models.Model):
    user = models.OneToOneField(CoreUser, on_delete=models.CASCADE, null=False)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    avatar = models.ImageField(blank=True, default="", upload_to="images/avatars")

    class Meta:
        abstract = True  # does not make the table, but you can inherit this model

    def __str__(self) -> str:
        return (
            self.first_name + " " + self.last_name + ", user pk: " + str(self.user.pk)
        )
