import factory
from core.models import CoreUser


class CoreUserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CoreUser

    email = factory.Faker("email")
    username = factory.SelfAttribute("email")  # same as 'email' by default
    password = factory.django.Password("plaintext_password")
