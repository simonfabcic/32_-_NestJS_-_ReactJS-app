# Generated by Django 5.0.2 on 2024-06-25 18:40

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("shop", "0007_alter_product_image"),
    ]

    operations = [
        migrations.AlterField(
            model_name="product",
            name="description",
            field=models.TextField(blank=True, null=True),
        ),
    ]
