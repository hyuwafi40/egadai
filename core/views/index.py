from core.views.base import BaseAuthView


class IndexViews(BaseAuthView):
    template_name = "core/index.html"
