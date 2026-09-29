from django.urls import path

from core.views import IndexViews

app_name = "core"

urlpatterns = [
    path("", IndexViews.as_view(), name="index"),
]
