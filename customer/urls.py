from django.urls import path

from customer.views import (
    CustomerCreateView,
    CustomerDeleteView,
    CustomerListView,
    CustomerUpdateView,
)

app_name = "customer"

urlpatterns = [
    path(
        "",
        CustomerListView.as_view(),
        name="list",
    ),
    path(
        "c/",
        CustomerCreateView.as_view(),
        name="create",
    ),
    path(
        "u/<int:pk>/",
        CustomerUpdateView.as_view(),
        name="update",
    ),
    path(
        "d/<int:pk>/",
        CustomerDeleteView.as_view(),
        name="delete",
    ),
]
