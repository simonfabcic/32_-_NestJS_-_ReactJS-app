import factory
from core.factory import CoreUserFactory
from shop.models import ShopProfile


class ShopProfileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ShopProfile

    user = factory.SubFactory(CoreUserFactory)
    first_name = factory.Faker("name")
    last_name = factory.Faker("last_name")
    avatar = factory.Faker("image_url")
