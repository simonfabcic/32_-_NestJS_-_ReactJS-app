from core.models import CoreProfile
from django.db import models

# Create your models here.


class ShopProfile(CoreProfile):
    def __str__(self) -> str:
        parent_string = super().__str__()
        return parent_string + ", prof. pk: " + str(self.pk)
