from django import forms
from django.contrib.auth import get_user_model

from account.utils.constants import DEFAULT_PASSWORD
from config.shared.forms import BaseModelForm

User = get_user_model()


class UserCreateForm(BaseModelForm):
    class Meta:
        model = User
        fields = ["username", "email", "job"]
        widgets = {
            "username": forms.TextInput(attrs={"placeholder": "Contoh: johndoe"}),
            "email": forms.EmailInput(
                attrs={"placeholder": "Contoh: john@example.com"}
            ),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(DEFAULT_PASSWORD)
        if commit:
            user.save()
            self._save_m2m()
        return user


class UserUpdateForm(BaseModelForm):
    class Meta:
        model = User
        fields = ["username", "email", "job"]
        widgets = {
            "username": forms.TextInput(attrs={"placeholder": "Contoh: johndoe"}),
            "email": forms.EmailInput(
                attrs={"placeholder": "Contoh: john@example.com"}
            ),
        }
