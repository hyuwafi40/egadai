from django.urls import path

from account.views import (
    ProfileDetailView,
    ProfileUpdateView,
    UserCreateView,
    UserDeleteView,
    UserListView,
    UserPasswordResetView,
    UserUpdateView,
)

app_name = "account"

urlpatterns = [
    path("profile/", ProfileDetailView.as_view(), name="profile-detail"),
    path("profile/u/", ProfileUpdateView.as_view(), name="profile-update"),
    path("user/", UserListView.as_view(), name="user-list"),
    path("user/c/", UserCreateView.as_view(), name="user-create"),
    path("user/u/<int:pk>/", UserUpdateView.as_view(), name="user-update"),
    path("user/d/<int:pk>/", UserDeleteView.as_view(), name="user-delete"),
    path("user/rp/<int:pk>/", UserPasswordResetView.as_view(), name="user-password-reset"),
]
