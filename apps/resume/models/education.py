from django.db import models
from modelcluster.fields import ParentalKey
from wagtail.admin.panels import FieldPanel
from wagtail.models import Orderable


class Education(Orderable):
    page = ParentalKey(
        "resume.ResumePage",
        on_delete=models.CASCADE,
        related_name="education_entries",
    )
    degree = models.CharField(max_length=255)
    institution = models.CharField(max_length=255)
    start_year = models.PositiveIntegerField(null=True, blank=True)
    end_year = models.PositiveIntegerField(null=True, blank=True)

    panels = [
        FieldPanel("degree"),
        FieldPanel("institution"),
        FieldPanel("start_year"),
        FieldPanel("end_year"),
    ]

    def __str__(self):
        return f"{self.degree} - {self.institution}"
