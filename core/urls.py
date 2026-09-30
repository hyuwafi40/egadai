from django.urls import path

from core.views import (
    BrandDetailView,
    BrandUpdateView,
    IndexViews,
    OrgsDetailView,
    OrgsUpdateView,
)

app_name = "core"

urlpatterns = [
    path("", IndexViews.as_view(), name="index"),
    path("brand/", BrandDetailView.as_view(), name="brand-detail"),
    path("brand/u/", BrandUpdateView.as_view(), name="brand-update"),
    path("orgs/", OrgsDetailView.as_view(), name="orgs-detail"),
    path("orgs/u/", OrgsUpdateView.as_view(), name="orgs-update"),
]
