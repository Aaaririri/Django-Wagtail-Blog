from django.db import models
from wagtail.admin.panels import FieldPanel, InlinePanel
from wagtail.fields import RichTextField
from wagtail.models import Page


class ResumePage(Page):
    summary = RichTextField(blank=True)
    pdf_file = models.ForeignKey(
        "wagtaildocs.Document",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Optional downloadable PDF version of the resume.",
    )

    max_count = 1
    parent_page_types = ["home.HomePage"]
    subpage_types = []

    content_panels = Page.content_panels + [
        FieldPanel("summary"),
        FieldPanel("pdf_file"),
        InlinePanel("experiences", label="Experience"),
        InlinePanel("education_entries", label="Education"),
        InlinePanel("skills", label="Skill"),
    ]
