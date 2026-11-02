from apps.home.api.static_json import StaticJSONView
from apps.blog.models import BlogPostPage


class BlogPostsJSONView(StaticJSONView):
    build_path = "api/posts.json"

    def get_data(self):
        posts = BlogPostPage.objects.live().public().order_by("-date")
        return [
            {
                "title": p.title,
                "slug": p.slug,
                "url": p.url,
                "date": p.date,
                "intro": p.intro,
                "tags": [t.name for t in p.tags.all()],
            }
            for p in posts
        ]
