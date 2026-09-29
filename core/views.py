from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView


class IndexViews(LoginRequiredMixin, TemplateView):
    template_name = "core/index.html"
