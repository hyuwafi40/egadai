from django.urls import path
from django.views.generic import RedirectView

from transaction.views import (
    TransactionDeleteView,
    TransactionDetailView,
    TransactionListView,
    TransactionNewView,
    TransactionPDFView,
    TransactionUpdateView,
)

app_name = "transaction"

urlpatterns = [
    path("", TransactionListView.as_view(), name="list"),
    path("new/", TransactionNewView.as_view(), name="new"),
    path(
        "c/",
        RedirectView.as_view(pattern_name="transaction:new", permanent=False),
        name="create",
    ),
    path("u/<int:pk>/", TransactionUpdateView.as_view(), name="update"),
    path("d/<int:pk>/", TransactionDeleteView.as_view(), name="delete"),
    path("<int:pk>/", TransactionDetailView.as_view(), name="detail"),
    path("<int:pk>/pdf/", TransactionPDFView.as_view(), name="pdf"),
]
