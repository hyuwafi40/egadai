from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views import View
from django.views.generic import CreateView, TemplateView, UpdateView

from customer.forms import CustomerForm
from customer.models import Customer
from customer.utils.constants import CUSTOMERS_PER_PAGE


class CustomerListView(LoginRequiredMixin, TemplateView):
    template_name = "customer/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = Customer.objects.all().order_by("name")
        paginator = Paginator(queryset, CUSTOMERS_PER_PAGE)
        page_obj = paginator.get_page(self.request.GET.get("page"))
        context["page_obj"] = page_obj
        context["total_customers"] = queryset.count()
        return context


class CustomerCreateView(LoginRequiredMixin, CreateView):
    model = Customer
    form_class = CustomerForm
    template_name = "customer/form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_title"] = "Tambah Nasabah"
        context["form_subtitle"] = "Buat data nasabah baru"
        return context

    def get_success_url(self):
        return reverse("customer:list")

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(
            self.request,
            f"Nasabah {form.instance.name} berhasil dibuat.",
        )
        return response

    def form_invalid(self, form):
        messages.error(
            self.request,
            "Periksa kembali data yang Anda masukkan.",
        )
        return super().form_invalid(form)


class CustomerUpdateView(LoginRequiredMixin, UpdateView):
    model = Customer
    form_class = CustomerForm
    template_name = "customer/form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_title"] = "Edit Nasabah"
        context["form_subtitle"] = "Perbarui data nasabah"
        return context

    def get_success_url(self):
        return reverse("customer:list")

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(
            self.request,
            f"Nasabah {form.instance.name} berhasil diperbarui.",
        )
        return response

    def form_invalid(self, form):
        messages.error(
            self.request,
            "Periksa kembali data yang Anda masukkan.",
        )
        return super().form_invalid(form)


class CustomerDeleteView(LoginRequiredMixin, View):
    http_method_names = ["post"]

    def post(self, request, pk, *args, **kwargs):
        target = get_object_or_404(Customer, pk=pk)
        name = target.name
        target.delete()
        return JsonResponse(
            {"success": True, "message": f"Nasabah {name} berhasil dihapus."}
        )
