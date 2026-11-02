import datetime

from django.core.management.base import BaseCommand
from wagtail.models import Page, Site

from apps.about.models import AboutPage, ContactLink
from apps.blog.models import BlogIndexPage, BlogPostPage
from apps.home.models import HomePage
from apps.resume.models import Education, Experience, ResumePage, Skill

SAMPLE_POST = """## Welcome

This post is written in **Markdown**.

- Lists work
- [Links](https://wagtail.org) work
- Images and GIFs: `![alt](https://example.com/image.gif)`

```python
print("hello, world")
```
"""


class Command(BaseCommand):
    help = "Create the initial home, about, resume and blog pages."

    def handle(self, *args, **options):
        if HomePage.objects.exists():
            self.stdout.write("Content already exists, nothing to do.")
            return

        root = Page.get_first_root_node()
        for welcome in root.get_children().exclude(content_type__model="homepage"):
            welcome.delete()

        home = root.add_child(
            instance=HomePage(
                title="Home",
                slug="home",
                hero_title="Hi, I'm Your Name",
                hero_subtitle="Developer, writer, and lifelong learner.",
            )
        )
        site = Site.objects.filter(is_default_site=True).first()
        if site:
            site.root_page = home
            site.save()
        else:
            Site.objects.create(
                hostname="localhost", port=80, root_page=home, is_default_site=True
            )

        about = home.add_child(
            instance=AboutPage(
                title="About me",
                slug="about",
                headline="A short line about who I am",
                email="you@example.com",
                location="Your City",
            )
        )
        ContactLink.objects.create(page=about, label="GitHub", url="https://github.com/")

        resume = home.add_child(instance=ResumePage(title="Resume", slug="resume"))
        Experience.objects.create(
            page=resume,
            role="Software Developer",
            company="Example Inc.",
            start_date=datetime.date(2022, 1, 1),
            description="Describe what you did.",
        )
        Education.objects.create(
            page=resume,
            degree="B.Sc. Computer Science",
            institution="Example University",
            start_year=2018,
            end_year=2022,
        )
        Skill.objects.create(page=resume, name="Python", category="Languages")

        blog = home.add_child(
            instance=BlogIndexPage(title="Blog", slug="blog", intro="Thoughts and notes.")
        )
        blog.add_child(
            instance=BlogPostPage(
                title="Hello, world",
                slug="hello-world",
                date=datetime.date.today(),
                intro="My first post.",
                body=[("markdown", SAMPLE_POST)],
            )
        )
        self.stdout.write(self.style.SUCCESS("Seed content created."))
