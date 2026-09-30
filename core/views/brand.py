from core.forms import BrandForm
from core.models import Brand
from core.views.base import (
    BaseDeveloperDetailView,
    BaseDeveloperUpdateView,
    SingletonObjectMixin,
    SingletonSuccessMixin,
)


class BrandDetailView(SingletonObjectMixin, BaseDeveloperDetailView):
    model = Brand
    template_name = "core/brand.html"
    context_object_name = "brand_obj"


class BrandUpdateView(
    SingletonObjectMixin,
    SingletonSuccessMixin,
    BaseDeveloperUpdateView,
):
    model = Brand
    form_class = BrandForm
    template_name = "core/brand/form.html"
    success_url_name = "core:brand-detail"
    success_message = "Brand berhasil diperbarui."
