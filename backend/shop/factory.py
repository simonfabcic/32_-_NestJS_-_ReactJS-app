import factory

from shop.models import ShopProfile
from core.factory import CoreUserFactory


class ShopProfileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ShopProfile

    user = factory.SubFactory(CoreUserFactory)
    first_name = factory.Faker("name")
    last_name = factory.Faker("last_name")
    avatar = factory.Faker("image_url")
