# Generated by Django 5.0.2 on 2024-06-22 19:11

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("shop", "0006_order_product_orderitem_order_products"),
    ]

    operations = [
        migrations.AlterField(
            model_name="product",
            name="image",
            field=models.ImageField(
                blank=True, default="", upload_to="images/products"
            ),
        ),
    ]
