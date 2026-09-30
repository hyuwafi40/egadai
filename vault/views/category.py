from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views import View

from vault.forms import CategoryForm
from vault.models import Category
from vault.utils.constants import CATEGORIES_PER_PAGE
from vault.views.base import BaseManagerView, ManagerRequiredMixin


class CategoryListView(BaseManagerView):
    template_name = "vault/category.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = Category.objects.all().order_by("name")
        paginator = Paginator(queryset, CATEGORIES_PER_PAGE)
        page_obj = paginator.get_page(self.request.GET.get("page"))
        context["page_obj"] = page_obj
        context["total_categories"] = queryset.count()
        return context


class CategoryCreateView(LoginRequiredMixin, ManagerRequiredMixin, View):
    http_method_names = ["post"]

    def post(self, request, *args, **kwargs):
        form = CategoryForm(request.POST)
        if not form.is_valid():
            return JsonResponse(
                {"success": False, "errors": form.errors.get_json_data()},
                status=400,
            )
        category = form.save()
        return JsonResponse(
            {
                "success": True,
                "message": f"Kategori {category.name} berhasil dibuat.",
            }
        )


class CategoryUpdateView(LoginRequiredMixin, ManagerRequiredMixin, View):
    http_method_names = ["post"]

    def post(self, request, pk, *args, **kwargs):
        target = get_object_or_404(Category, pk=pk)
        form = CategoryForm(request.POST, instance=target)
        if not form.is_valid():
            return JsonResponse(
                {"success": False, "errors": form.errors.get_json_data()},
                status=400,
            )
        category = form.save()
        return JsonResponse(
            {
                "success": True,
                "message": f"Kategori {category.name} berhasil diperbarui.",
            }
        )


class CategoryDeleteView(LoginRequiredMixin, ManagerRequiredMixin, View):
    http_method_names = ["post"]

    def post(self, request, pk, *args, **kwargs):
        target = get_object_or_404(Category, pk=pk)
        name = target.name
        target.delete()
        return JsonResponse(
            {"success": True, "message": f"Kategori {name} berhasil dihapus."}
        )
