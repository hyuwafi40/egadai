from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, TemplateView, UpdateView


class BaseView(TemplateView):
    pass


class BaseAuthView(LoginRequiredMixin, TemplateView):
    pass


class BaseAuthDetailView(LoginRequiredMixin, DetailView):
    pass


class BaseAuthUpdateView(LoginRequiredMixin, UpdateView):
    pass
