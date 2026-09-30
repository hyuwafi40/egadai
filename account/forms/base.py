from config.shared.forms import ClearableImageForm


class BasePhotoModelForm(ClearableImageForm):
    image_field_name = "photo"
    image_label = "foto"
