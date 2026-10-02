MANAGER_ROLES = ("developer", "administrator")


def user_is_manager(user):
    if not user or not getattr(user, "is_authenticated", False):
        return False
    if getattr(user, "is_superuser", False):
        return True
    job = getattr(user, "job", None)
    return job in MANAGER_ROLES
