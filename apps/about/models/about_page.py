from django.db import models
from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.fields import RichTextField
from wagtail.models import Page


class AboutPage(Page):
    headline = models.CharField(max_length=255, blank=True)
    photo = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    bio = RichTextField(blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=50, blank=True)
    location = models.CharField(max_length=255, blank=True)

    max_count = 1
    parent_page_types = ["home.HomePage"]
    subpage_types = []

    content_panels = Page.content_panels + [
        FieldPanel("headline"),
        FieldPanel("photo"),
        FieldPanel("bio"),
        MultiFieldPanel(
            [FieldPanel("email"), FieldPanel("phone"), FieldPanel("location")],
            heading="Contact information",
        ),
        InlinePanel("contact_links", label="Contact link"),
    ]
