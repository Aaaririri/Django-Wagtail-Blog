from apps.home.api.static_json import StaticJSONView
from apps.about.models import AboutPage


class AboutJSONView(StaticJSONView):
    build_path = "api/about.json"

    def get_data(self):
        page = AboutPage.objects.live().first()
        if page is None:
            return {}
        return {
            "title": page.title,
            "headline": page.headline,
            "email": page.email,
            "phone": page.phone,
            "location": page.location,
            "links": [{"label": l.label, "url": l.url} for l in page.contact_links.all()],
        }
