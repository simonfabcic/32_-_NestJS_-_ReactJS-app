from io import BytesIO

import factory
from core.factory import CoreUserFactory
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image
from shop.models import Product, ShopProfile


class ShopProfileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ShopProfile

    user = factory.SubFactory(CoreUserFactory)
    first_name = factory.Faker("name")
    last_name = factory.Faker("last_name")

    @factory.lazy_attribute
    def avatar(self):
        binary_stream = BytesIO()
        Image.new("RGB", (100, 100)).save(binary_stream, format="JPEG")
        binary_stream.seek(0)
        return SimpleUploadedFile(
            "test_avatar.jpg", binary_stream.read(), content_type="image/jpeg"
        )


class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product

    @factory.lazy_attribute
    def image(self):
        # create an in-memory image
        binary_stream = BytesIO()
        Image.new("RGB", (100, 100)).save(binary_stream, format="JPEG")
        # sets the file pointer to the beginning of the BytesIO object
        binary_stream.seek(0)
        return SimpleUploadedFile(
            "test_image.jpg", binary_stream.read(), content_type="image/jpeg"
        )

    # image = factory.Faker("image_url")
    title = factory.Faker("word")
    description = factory.Faker("sentence")
    price = factory.Faker(
        "pydecimal",
        min_value=10,
        max_value=1000000,
        right_digits=2,
        positive=True,
    )
