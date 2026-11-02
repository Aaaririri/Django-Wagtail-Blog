from django.db import models
from modelcluster.fields import ParentalKey
from wagtail.admin.panels import FieldPanel
from wagtail.models import Orderable


class Experience(Orderable):
    page = ParentalKey(
        "resume.ResumePage", on_delete=models.CASCADE, related_name="experiences"
    )
    role = models.CharField(max_length=255)
    company = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True, help_text="Leave empty if current.")
    description = models.TextField(blank=True)

    panels = [
        FieldPanel("role"),
        FieldPanel("company"),
        FieldPanel("start_date"),
        FieldPanel("end_date"),
        FieldPanel("description"),
    ]

    def __str__(self):
        return f"{self.role} at {self.company}"
