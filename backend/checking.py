import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")
django.setup()

print("start testing")

from core.models import User
from shop.models import Profile, Role

# profile_first = Profile.objects.first()

# users = User.objects.all()
# print(users)

#### Creating 'shop profile'
# profile = Profile()
# profile.user = users[0]
# profile.first_name = "John"
# profile.last_name = "Doe"
# profile.save()
# print(profile)

#### Creating 'shop Role'
# role = Role()
# role.name = "Administrator"
# role.save()

#### Creating 'User'
# user1 = User()
# user1.email = "user1@email.com"
# user1.password = "UserPassword123"
# user1.username = "johanna"
# user1.save()

#### Getting 'Role'
# role_administrator = Role.objects.get(name="Administrator")

#### Getting 'User'
# user_admin = User.objects.get(username="admin")

#### Getting 'shop Profile'
# profile = Profile.objects.first()
# print(profile.role)

#### Creating 'shop Profile'
# profile = Profile()
# profile.role = role_administrator
# profile.user = user1
# profile.first_name = "Simon"
# profile.last_name = "Smith"
# profile.save()

#### Getting  all 'Core-Profile' objects and printing them out
# user_admin = User.objects.get(username="admin")
# profile_admin = user_admin.profile
# email_admin = user_admin.email
# username_admin = user_admin.username
# user_profile_admin = profile_admin.user
# first_name_admin = profile_admin.first_name
# last_name_admin = profile_admin.last_name
# role_admin = profile_admin.role # this does not work because 'profile_admin' is instance of  class 'core.models.Profile' and not 'shop.models.Profile'

# print (
#   "user_admin: ", user_admin,
#   "\nprofile_admin: ", profile_admin,
#   "\nemail_admin: ", email_admin,
#   "\nusername_admin: ", username_admin,
#   "\nuser_profile_admin: ", user_profile_admin,
#   "\nfirst_name_admin: ", first_name_admin,
#   "\nlast_name_admin: ", last_name_admin,
#   # "\nrole_admin: ", role_admin, # not accessible
#   )

#### Creating user with password and adding connect it to the 'Shop-profile'
# user = User.objects.create_user(
#   username='john',
#   email='jlennon@beatles.com',
#   password='glass onion')

# profile = Profile.objects.create(
#   user = User.objects.get(username="john"),
#   role = role_administrator,
#   first_name = "John",
#   last_name = "Lennon",
# )


# profile = Profile.objects.create(user=User.objects.get(username="john"), first_name='John', last_name='Doe')

#### Creating profile
# profile = Profile.objects.create(
#   user = User.objects.get(username="john"),
#   role = role_administrator,
#   first_name = "John",
#   last_name = "Lennon",
# )

#### Getting profile according to username
profile = Profile.objects.first()
print("Profile of admin: ", profile.user.username)

profile = Profile.objects.get(user=User.objects.get(username="johanna"))
profile = Profile.objects.get(user__username="johanna")
