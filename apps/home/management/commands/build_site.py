import re
from pathlib import Path

from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand

ATTR_RE = re.compile(r'(\s(?:href|src|action|poster|content)=")/(?!/)')
SRCSET_RE = re.compile(r'(srcset=")/(?!/)')


class Command(BaseCommand):
    help = "Build the static site into BUILD_DIR and prefix root-relative URLs with SITE_BASE_PATH."

    def handle(self, *args, **options):
        call_command("collectstatic", interactive=False, verbosity=0)
        call_command("build")
        base = settings.BASE_PATH
        if not base:
            return
        prefix = f"/{base}/"
        count = 0
        for html in Path(settings.BUILD_DIR).rglob("*.html"):
            text = html.read_text(encoding="utf-8")
            new = ATTR_RE.sub(lambda m: m.group(1) + prefix, text)
            new = SRCSET_RE.sub(lambda m: m.group(1) + prefix, new)
            if new != text:
                html.write_text(new, encoding="utf-8")
                count += 1
        self.stdout.write(f"Prefixed URLs with {prefix} in {count} files.")
