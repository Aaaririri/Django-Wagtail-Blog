from django.conf import settings
from wagtail.models import Page

from .static_json import StaticJSONView


class SiteJSONView(StaticJSONView):
    build_path = "api/site.json"

    def get_data(self):
        pages = Page.objects.live().public().not_type(Page).specific() if False else None
        pages = Page.objects.live().public().exclude(depth=1)
        return {
            "site_name": settings.SITE_NAME,
            "pages": [
                {"title": p.title, "type": p.specific_class.__name__, "path": p.url}
                for p in pages
            ],
        }
