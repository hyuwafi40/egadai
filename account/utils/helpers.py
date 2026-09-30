def normalize_email(email):
    if not email:
        return email
    return email.strip().lower()


def normalize_username(username):
    if not username:
        return username
    return username.strip().lower()


def profile_cache_key(user_id):
    return f"account.profile.{user_id}"
