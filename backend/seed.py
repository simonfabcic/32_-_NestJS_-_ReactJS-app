import os
import random

import django
from configurations import importer
from core.models import CoreUser
from shop.models import Role, ShopProfile

os.environ.setdefault("DJANGO_CONFIGURATION", "Dev")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")

importer.install()

django.setup()


print("Start seeding...")


ROLES = [
    "Administrator",
    "User",
    "Manager",
    "Supervisor",
    "Analyst",
    "Auditor",
    "Moderator",
]

for role in ROLES:
    if not Role.objects.filter(name=role).exists():
        Role.objects.create(name=role)

FIRST_NAMES = [
    "John",
    "Jane",
    "Michael",
    "Emily",
    "William",
    "Olivia",
    "James",
    "Sophia",
    "Benjamin",
    "Isabella",
    "Jacob",
    "Emma",
    "Elijah",
    "Ava",
    "Matthew",
    "Mia",
    "David",
    "Charlotte",
    "Daniel",
    "Amelia",
    "Alexander",
    "Harper",
    "Joseph",
    "Evelyn",
    "Samuel",
    "Abigail",
    "Henry",
    "Victoria",
    "Luke",
    "Grace",
]

LAST_NAMES = [
    "Smith",
    "Johnson",
    "Williams",
    "Jones",
    "Brown",
    "Davis",
    "Miller",
    "Wilson",
    "Moore",
    "Taylor",
    "Anderson",
    "Thomas",
    "Jackson",
    "White",
    "Harris",
    "Martin",
    "Thompson",
    "Garcia",
    "Martinez",
    "Robinson",
    "Clark",
    "Rodriguez",
    "Lewis",
    "Lee",
    "Walker",
    "Hall",
    "Allen",
    "Young",
    "Hernandez",
    "King",
]

for i in range(100):
    selected_first_name = random.choice(FIRST_NAMES)
    selected_last_name = random.choice(LAST_NAMES)
    email = (
        selected_first_name.lower() + "." + selected_last_name.lower() + "@example.com"
    )

    try:
        user = CoreUser.objects.create_user(
            username=email,
            email=email,
            password="asdfggfdsa",
        )
    except Exception:
        print(i, ". user skipped. User wasn't created.")
    else:
        ShopProfile.objects.create(
            user=user,
            role=Role.objects.get(name=random.choice(ROLES)),
            first_name=selected_first_name,
            last_name=selected_last_name,
        )
        print(i, ". user created with profile.")
