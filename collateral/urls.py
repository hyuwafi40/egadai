from django.urls import path

from collateral.views import (
    CollateralCreateView,
    CollateralDeleteView,
    CollateralListView,
    CollateralUpdateView,
)

app_name = "collateral"

urlpatterns = [
    path(
        "",
        CollateralListView.as_view(),
        name="list",
    ),
    path(
        "c/",
        CollateralCreateView.as_view(),
        name="create",
    ),
    path(
        "u/<int:pk>/",
        CollateralUpdateView.as_view(),
        name="update",
    ),
    path(
        "d/<int:pk>/",
        CollateralDeleteView.as_view(),
        name="delete",
    ),
]
