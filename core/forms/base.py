from django import forms

GLASS_WIDGETS = (
    forms.TextInput,
    forms.EmailInput,
    forms.URLInput,
    forms.NumberInput,
    forms.PasswordInput,
    forms.Textarea,
    forms.FileInput,
    forms.DateInput,
    forms.DateTimeInput,
    forms.TimeInput,
    forms.Select,
    forms.SelectMultiple,
)


class BaseModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            widget = field.widget
            if isinstance(widget, GLASS_WIDGETS):
                existing = widget.attrs.get("class", "")
                if "glass-input" not in existing:
                    widget.attrs["class"] = (existing + " glass-input").strip()


class BaseLogoModelForm(BaseModelForm):
    clear_logo = forms.BooleanField(
        required=False,
        label="Hapus logo saat ini",
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"}),
    )

    def save(self, commit=True):
        instance = super().save(commit=False)
        if not hasattr(instance, "logo"):
            if commit:
                instance.save()
                self._save_m2m()
            return instance
        if self.cleaned_data.get("clear_logo") and not self.cleaned_data.get("logo"):
            instance.logo = None
        if commit:
            instance.save()
            self._save_m2m()
        return instance
