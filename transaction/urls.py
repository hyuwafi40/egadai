from django.urls import path

from transaction.views import (
    TransactionCreateView,
    TransactionDeleteView,
    TransactionListView,
    TransactionUpdateView,
)

app_name = "transaction"

urlpatterns = [
    path(
        "",
        TransactionListView.as_view(),
        name="list",
    ),
    path(
        "c/",
        TransactionCreateView.as_view(),
        name="create",
    ),
    path(
        "u/<int:pk>/",
        TransactionUpdateView.as_view(),
        name="update",
    ),
    path(
        "d/<int:pk>/",
        TransactionDeleteView.as_view(),
        name="delete",
    ),
]
