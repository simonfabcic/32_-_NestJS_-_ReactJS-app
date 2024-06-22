import factory
from core.factory import CoreUserFactory
from shop.models import Product, ShopProfile


class ShopProfileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ShopProfile

    user = factory.SubFactory(CoreUserFactory)
    first_name = factory.Faker("name")
    last_name = factory.Faker("last_name")
    avatar = factory.Faker("image_url")


class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product

    image = factory.Faker("image_url")
    title = factory.Faker("word")
    description = factory.Faker("sentence")
    price = factory.Faker(
        "pydecimal",
        min_value=10,
        max_value=1000000,
        right_digits=2,
        positive=True,
    )
