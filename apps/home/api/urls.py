from django.urls import path

from apps.about.api.views import AboutJSONView
from apps.blog.api.views import BlogPostsJSONView
from apps.home.api.views import SiteJSONView
from apps.resume.api.views import ResumeJSONView

urlpatterns = [
    path("site.json", SiteJSONView.as_view(), name="api-site"),
    path("about.json", AboutJSONView.as_view(), name="api-about"),
    path("resume.json", ResumeJSONView.as_view(), name="api-resume"),
    path("posts.json", BlogPostsJSONView.as_view(), name="api-posts"),
]
