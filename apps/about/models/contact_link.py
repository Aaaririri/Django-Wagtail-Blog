from django.db import models
from modelcluster.fields import ParentalKey
from wagtail.admin.panels import FieldPanel
from wagtail.models import Orderable


class ContactLink(Orderable):
    page = ParentalKey(
        "about.AboutPage", on_delete=models.CASCADE, related_name="contact_links"
    )
    label = models.CharField(max_length=100)
    url = models.URLField()

    panels = [FieldPanel("label"), FieldPanel("url")]

    def __str__(self):
        return self.label
