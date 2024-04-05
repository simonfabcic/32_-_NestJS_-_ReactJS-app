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
  # role = CharField(source='role.name') # error if attribute not present
  role = SerializerMethodField()
  username = CharField(source='user.username')

  class Meta:
    model = Profile
    fields = [
      'id',
      'email',
      'full_name',
      'first_name',
      'last_name',
      'role',
      'username',
      # 'actions',
    ]

  def get_role(self, obj):
    return obj.role.name if obj.role else None
  
  def get_full_name(self, obj):
    return f"{obj.first_name} {obj.last_name}"