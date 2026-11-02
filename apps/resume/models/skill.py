from django.db import models
from modelcluster.fields import ParentalKey
from wagtail.admin.panels import FieldPanel
from wagtail.models import Orderable


class Skill(Orderable):
    page = ParentalKey(
        "resume.ResumePage", on_delete=models.CASCADE, related_name="skills"
    )
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=100, blank=True)

    panels = [FieldPanel("name"), FieldPanel("category")]

    def __str__(self):
        return self.name
