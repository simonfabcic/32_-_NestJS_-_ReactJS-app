def can_view_groups(user):
    return (
        user.is_superuser
        or user.has_perm("auth.change_group")
        or user.has_perm("auth.view_group")
    )


def can_view_products(user):
    return (
        user.is_superuser
        or user.has_perm("shop.change_product")
        or user.has_perm("shop.view_product")
    )
