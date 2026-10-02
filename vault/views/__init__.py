from vault.views.base import (
    BaseManagerCreateView,
    BaseManagerUpdateView,
    BaseManagerView,
    ManagerRequiredMixin,
)
from vault.views.category import (
    CategoryCreateView,
    CategoryDeleteView,
    CategoryListView,
    CategoryUpdateView,
)
from vault.views.scheme import (
    SchemeCreateView,
    SchemeDeleteView,
    SchemeListView,
    SchemeUpdateView,
)
from vault.views.storages import (
    StoragesCreateView,
    StoragesDeleteView,
    StoragesListView,
    StoragesUpdateView,
)

__all__ = [
    "BaseManagerCreateView",
    "BaseManagerUpdateView",
    "BaseManagerView",
    "CategoryCreateView",
    "CategoryDeleteView",
    "CategoryListView",
    "CategoryUpdateView",
    "ManagerRequiredMixin",
    "SchemeCreateView",
    "SchemeDeleteView",
    "SchemeListView",
    "SchemeUpdateView",
    "StoragesCreateView",
    "StoragesDeleteView",
    "StoragesListView",
    "StoragesUpdateView",
]
