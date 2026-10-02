from django.urls import path

from payment.views import (
    PaymentChooseView,
    PaymentCreateView,
    PaymentDeleteView,
    PaymentDetailView,
    PaymentListView,
    PaymentPDFView,
)

app_name = "payment"

urlpatterns = [
    path("", PaymentListView.as_view(), name="list"),
    path("choose/", PaymentChooseView.as_view(), name="choose"),
    path(
        "new/<int:transaction_pk>/",
        PaymentCreateView.as_view(),
        name="create",
    ),
    path("<int:pk>/", PaymentDetailView.as_view(), name="detail"),
    path("<int:pk>/pdf/", PaymentPDFView.as_view(), name="pdf"),
    path("<int:pk>/d/", PaymentDeleteView.as_view(), name="delete"),
]
