from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path
from django.views.static import serve

from config import views

urlpatterns = [
    path("", views.IndexViews.as_view(), name="login"),
    path("admin/", admin.site.urls),
    path("core/", include(("core.urls", "core"), namespace="core")),
    path("account/", include(("account.urls", "account"), namespace="account")),
    path("vault/", include(("vault.urls", "vault"), namespace="vault")),
    path("logout/", views.logout_view, name="logout"),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
else:
    urlpatterns += [
        re_path(r"^media/(?P<path>.*)$", serve, {"document_root": settings.MEDIA_ROOT}),
    ]
