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


class ClearableImageForm(BaseModelForm):
    image_field_name = "image"
    image_label = "gambar"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        clear_name = f"clear_{self.image_field_name}"
        if clear_name not in self.fields:
            self.fields[clear_name] = forms.BooleanField(
                required=False,
                label=f"Hapus {self.image_label} saat ini",
                widget=forms.CheckboxInput(attrs={"class": "form-check-input"}),
            )

    def save(self, commit=True):
        instance = super().save(commit=False)
        field = self.image_field_name
        if hasattr(instance, field):
            clear_name = f"clear_{field}"
            if self.cleaned_data.get(clear_name) and not self.cleaned_data.get(field):
                setattr(instance, field, None)
        if commit:
            instance.save()
            self._save_m2m()
        return instance
