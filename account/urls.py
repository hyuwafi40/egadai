from django.urls import path

from account.views import ProfileDetailView, ProfileUpdateView

app_name = "account"

urlpatterns = [
    path("profile/", ProfileDetailView.as_view(), name="profile-detail"),
    path("profile/u/", ProfileUpdateView.as_view(), name="profile-update"),
]
