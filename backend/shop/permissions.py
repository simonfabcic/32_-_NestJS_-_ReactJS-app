def can_view_groups(user):
    return (
        user.is_superuser
        or user.has_perm("auth.change_group")
        or user.has_perm("auth.view_group")
    )


def can_create_groups(user):
    return user.is_superuser or user.has_perm("auth.change_group")
