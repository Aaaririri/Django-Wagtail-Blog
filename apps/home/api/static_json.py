import json

from bakery.views import BuildableTemplateView
from django.http import HttpResponse


class StaticJSONView(BuildableTemplateView):
    build_path = ""

    def get_data(self):
        raise NotImplementedError

    def get(self, request, *args, **kwargs):
        return HttpResponse(
            json.dumps(self.get_data(), indent=2, default=str),
            content_type="application/json",
        )

    def get_content(self):
        return self.get(self.request).content
