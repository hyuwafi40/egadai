from django.db import transaction

from account.models import User
from account.utils.constants import JobChoices


def create_user_with_profile(
    username,
    email,
    password,
    profile_data=None,
    **kwargs,
):
    with transaction.atomic():
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            **kwargs,
        )
        if profile_data:
            profile = user.profile
            for field, value in profile_data.items():
                setattr(profile, field, value)
            profile.save()
    return user


def change_job(user, job):
    if job not in JobChoices.values:
        raise ValueError(f"Job tidak valid: {job}")
    user.job = job
    user.save()
    return user
