from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.contrib.auth.models import Group, Permission, AbstractUser


@receiver(m2m_changed, sender=AbstractUser.user_permissions.through)
def manage_related_permissions(
    sender, instance, action, reverse, model, pk_set, **kwargs
):
    """
    Because of business logic,
    we need to ensure that `change_` role always comes with `view_` role.
    If `view_` permission is removed, the `change_` permission is removed as well.
    """

    # Check if the 'instance' is a 'AbstractUser', because signal is triggered also when 'permission' is added to 'Group'
    if not isinstance(instance, AbstractUser):
        return

    permission_change_role = Permission.objects.get(codename="change_role")
    permission_view_role = Permission.objects.get(codename="view_role")
    if action == "post_add":
        if permission_change_role.id in pk_set:
            instance.user_permissions.add(permission_view_role)

    elif action == "post_remove":
        if permission_view_role.id in pk_set:
            instance.user_permissions.remove(permission_change_role)


@receiver(m2m_changed, sender=Group.permissions.through)
def manage_related_permission_in_group(
    sender, instance, action, reverse, model, pk_set, **kwargs
):
    """
    Because of business logic,
    we need to ensure that `change_` role always comes with `view_` role.
    If `view_` permission is removed, the `change_` permission is removed as well.
    """
    if not isinstance(instance, Group):
        return

    permission_change_role = Permission.objects.get(codename="change_role")
    permission_view_role = Permission.objects.get(codename="view_role")
    if action == "post_add":
        if permission_change_role.id in pk_set:
            instance.permissions.add(permission_view_role)

    elif action == "post_remove":
        if permission_view_role.id in pk_set:
            instance.permissions.remove(permission_change_role)
