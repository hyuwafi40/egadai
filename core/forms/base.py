from config.shared.forms import ClearableImageForm


class BaseLogoModelForm(ClearableImageForm):
    image_field_name = "logo"
    image_label = "logo"
