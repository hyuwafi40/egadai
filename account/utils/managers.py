from django.contrib.auth.models import BaseUserManager

from account.utils.constants import DEFAULT_JOB, JobChoices
from account.utils.helpers import normalize_email, normalize_username


class UserManager(BaseUserManager):
    def _create_user(self, username, email, password, **extra):
        if not username:
            raise ValueError("Username wajib diisi.")
        if not email:
            raise ValueError("Email wajib diisi.")
        email = normalize_email(email)
        username = normalize_username(username)
        user = self.model(
            username=username,
            email=email,
            **extra,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email, password=None, **extra):
        extra.setdefault("job", DEFAULT_JOB)
        return self._create_user(
            username,
            email,
            password,
            **extra,
        )

    def create_superuser(
        self,
        username,
        email,
        password=None,
        **extra,
    ):
        extra["job"] = JobChoices.DEVELOPER
        extra["is_staff"] = True
        extra["is_superuser"] = True
        extra["is_active"] = True
        return self._create_user(
            username,
            email,
            password,
            **extra,
        )
