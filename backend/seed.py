import os
import django
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

print("Start seeding...")

from core.models import User
from shop.models import Profile, Role

ROLES = ["Administrator", "User", "Manager", "Supervisor", "Analyst", "Auditor", "Moderator",]

for role in ROLES:
  if not Role.objects.filter(name=role).exists():
    Role.objects.create(name=role)

FIRST_NAMES = [
    'John', 'Jane', 'Michael', 'Emily', 'William', 'Olivia', 'James', 'Sophia', 'Benjamin', 'Isabella',
    'Jacob', 'Emma', 'Elijah', 'Ava', 'Matthew', 'Mia', 'David', 'Charlotte', 'Daniel', 'Amelia',
    'Alexander', 'Harper', 'Joseph', 'Evelyn', 'Samuel', 'Abigail', 'Henry', 'Victoria', 'Luke', 'Grace'
]
LAST_NAMES = [
    'Smith', 'Johnson', 'Williams', 'Jones', 'Brown', 'Davis', 'Miller', 'Wilson', 'Moore', 'Taylor',
    'Anderson', 'Thomas', 'Jackson', 'White', 'Harris', 'Martin', 'Thompson', 'Garcia', 'Martinez', 'Robinson',
    'Clark', 'Rodriguez', 'Lewis', 'Lee', 'Walker', 'Hall', 'Allen', 'Young', 'Hernandez', 'King'
]

selected_first_name = random.choice(FIRST_NAMES)
selected_last_name = random.choice(LAST_NAMES)
username = (selected_first_name + "_" + selected_last_name).lower()

for i in range(100):
  selected_first_name = random.choice(FIRST_NAMES)
  selected_last_name = random.choice(LAST_NAMES)
  username = (selected_first_name + "_" + selected_last_name).lower()

  try:
    user = User.objects.create_user(
      username = username,
      email = selected_first_name.lower() + "." + selected_last_name.lower() + "@email.com",
      password = "asdfggfdsa"
    )
  except:
    print(i, ". user skipped. Profile wasn't created.")
  else:
    Profile.objects.create(
      user = user,
      role = Role.objects.get(name=random.choice(ROLES)),
      first_name = selected_first_name,
      last_name = selected_last_name,
    )
    print(i, ". user created with profile.")