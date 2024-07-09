from core.models import CoreProfile
from django.db import models

# Create your models here.


class ShopProfile(CoreProfile):
    def __str__(self) -> str:
        parent_string = super().__str__()
        return parent_string + ", prof. pk: " + str(self.pk)


class Order(models.Model):
    products = models.ManyToManyField("Product", through="OrderItem")
    buyer = models.ForeignKey(ShopProfile, on_delete=models.CASCADE, null=False)


class Product(models.Model):
    image = models.ImageField(
        blank=True, null=True, default="", upload_to="images/products"
    )
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, default="")
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self) -> str:
        return f"{self.title}, {self.price} $"


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name="order_items"
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    class Meta:
        unique_together = ("order", "product")
