from django.db import models
from modelcluster.contrib.taggit import ClusterTaggableManager
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.fields import StreamField
from wagtail.models import Page

from apps.blog.blocks import PostBodyBlock
from .blog_post_tag import BlogPostTag


class BlogPostPage(Page):
    date = models.DateField("Post date")
    intro = models.CharField(max_length=250, blank=True)
    cover_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    body = StreamField(PostBodyBlock(), blank=True)
    tags = ClusterTaggableManager(through=BlogPostTag, blank=True)

    parent_page_types = ["blog.BlogIndexPage"]
    subpage_types = []

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [FieldPanel("date"), FieldPanel("tags")], heading="Post information"
        ),
        FieldPanel("intro"),
        FieldPanel("cover_image"),
        FieldPanel("body"),
    ]
