import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

print("start testing")

from core.models import *

#profile_first = Profile.objects.first()

# users = User.objects.all()
# print(users)

# profile = Profile()
# profile.user = users[0]
# profile.first_name = "John"
# profile.last_name = "Doe"
# profile.save()

# print(profile)







user_admin = User.objects.get(username="admin")
profile_admin = user_admin.profile
email_admin = user_admin.email
username_admin = user_admin.username
user_profile_admin = profile_admin.user
first_name_admin = profile_admin.first_name
last_name_admin = profile_admin.last_name
role_admin = profile_admin.role

print (
  "user_admin: ", user_admin,
  "\nprofile_admin: ", profile_admin,
  "\nemail_admin: ", email_admin,
  "\nusername_admin: ", username_admin,
  "\nuser_profile_admin: ", user_profile_admin,
  "\nfirst_name_admin: ", first_name_admin,
  "\nlast_name_admin: ", last_name_admin,
  "\nrole_admin: ", role_admin,
  )