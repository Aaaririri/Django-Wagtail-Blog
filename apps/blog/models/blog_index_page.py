from wagtail.admin.panels import FieldPanel
from wagtail.fields import RichTextField
from wagtail.models import Page

from .blog_post_page import BlogPostPage


class BlogIndexPage(Page):
    intro = RichTextField(blank=True)

    max_count = 1
    parent_page_types = ["home.HomePage"]
    subpage_types = ["blog.BlogPostPage"]

    content_panels = Page.content_panels + [FieldPanel("intro")]

    def get_posts(self):
        return (
            BlogPostPage.objects.child_of(self)
            .live()
            .order_by("-date", "-first_published_at")
        )

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context["posts"] = self.get_posts()
        return context

