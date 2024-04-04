from django.db import models
from core.models import Profile

# Create your models here.

class Role(models.Model):
  name=models.CharField(max_length=20)

  def __str__(self) -> str:
    return self.name

class Profile(Profile):
  role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True)

  def __str__(self) -> str:
    parent_string = super().__str__()
    return (parent_string + ", prof. pk: " + str(self.pk))