from django.urls import path

from vault.views import (
    CategoryCreateView,
    CategoryDeleteView,
    CategoryListView,
    CategoryUpdateView,
)

app_name = "vault"

urlpatterns = [
    path("category/", CategoryListView.as_view(), name="category-list"),
    path("category/c/", CategoryCreateView.as_view(), name="category-create"),
    path("category/u/<int:pk>/", CategoryUpdateView.as_view(), name="category-update"),
    path("category/d/<int:pk>/", CategoryDeleteView.as_view(), name="category-delete"),
]
