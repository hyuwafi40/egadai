from django.urls import path

from vault.views import (
    CategoryCreateView,
    CategoryDeleteView,
    CategoryListView,
    CategoryUpdateView,
    SchemeCreateView,
    SchemeDeleteView,
    SchemeListView,
    SchemeUpdateView,
)

app_name = "vault"

urlpatterns = [
    path(
        "category/",
        CategoryListView.as_view(),
        name="category-list",
    ),
    path(
        "category/c/",
        CategoryCreateView.as_view(),
        name="category-create",
    ),
    path(
        "category/u/<int:pk>/",
        CategoryUpdateView.as_view(),
        name="category-update",
    ),
    path(
        "category/d/<int:pk>/",
        CategoryDeleteView.as_view(),
        name="category-delete",
    ),
    path(
        "scheme/",
        SchemeListView.as_view(),
        name="scheme-list",
    ),
    path(
        "scheme/c/",
        SchemeCreateView.as_view(),
        name="scheme-create",
    ),
    path(
        "scheme/u/<int:pk>/",
        SchemeUpdateView.as_view(),
        name="scheme-update",
    ),
    path(
        "scheme/d/<int:pk>/",
        SchemeDeleteView.as_view(),
        name="scheme-delete",
    ),
]
