from core.views.base import (
    BaseAuthView,
    BaseDeveloperDetailView,
    BaseDeveloperView,
    BaseDeveloperUpdateView,
    BaseManagerDetailView,
    BaseManagerUpdateView,
    BaseManagerView,
    BaseRegulerView,
    BaseView,
    SingletonObjectMixin,
    SingletonSuccessMixin,
)
from core.views.brand import BrandDetailView, BrandUpdateView
from core.views.index import IndexViews
from core.views.orgs import OrgsDetailView, OrgsUpdateView

__all__ = [
    "BaseAuthView",
    "BaseDeveloperDetailView",
    "BaseDeveloperView",
    "BaseDeveloperUpdateView",
    "BaseManagerDetailView",
    "BaseManagerUpdateView",
    "BaseManagerView",
    "BaseRegulerView",
    "BaseView",
    "BrandDetailView",
    "BrandUpdateView",
    "IndexViews",
    "OrgsDetailView",
    "OrgsUpdateView",
    "SingletonObjectMixin",
    "SingletonSuccessMixin",
]
