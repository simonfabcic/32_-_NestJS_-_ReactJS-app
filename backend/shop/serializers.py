from rest_framework.serializers import ModelSerializer, EmailField, CharField, SerializerMethodField
from shop.models import Profile, Role

class RoleSerializer(ModelSerializer):
  class Meta:
    model = Role
    fields = [
      'name'
    ]

class ProfileSerializer(ModelSerializer):
  email = EmailField(source='user.email')
  full_name = SerializerMethodField()
  role = CharField(source='role.name')
  # actions = "Actions - hard coded" # TODO
  class Meta:
    model = Profile
    fields = [
      'id',
      'email',
      'full_name',
      'role',
      # 'actions',
    ]

  def get_full_name(self, obj):
      return f"{obj.first_name} {obj.last_name}"