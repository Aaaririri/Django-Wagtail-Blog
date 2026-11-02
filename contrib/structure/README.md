# Project Structure

A Wagtail blog exported as a static site and deployed to GitHub Pages.

```
Django-Wagtail-Blog/
├── manage.py
├── requirements.txt
├── db.sqlite3                  # content database (commit it: CI builds from it)
├── media/                      # uploaded images, GIFs, videos, documents (commit it)
├── config/                     # project settings, urls, wsgi, context processors
├── templates/                  # global templates (base, includes, 404)
├── static/css/site.css         # global styles
├── .github/workflows/deploy.yml
└── apps/
    ├── home/                   # Home page + shared tooling
    │   ├── models/home_page.py
    │   ├── api/                # static JSON helpers, site.json, API url routes
    │   ├── templates/home/
    │   └── management/commands/{seed_content,build_site}.py
    ├── about/                  # About me / contact information
    │   ├── models/{about_page,contact_link}.py
    │   ├── api/                # about.json
    │   └── templates/about/
    ├── resume/                 # Resume
    │   ├── models/{resume_page,experience,education,skill}.py
    │   ├── api/                # resume.json
    │   └── templates/resume/
    └── blog/                   # Blog posts
        ├── blocks.py           # StreamField blocks (Markdown, image/GIF, video, code...)
        ├── models/{blog_index_page,blog_post_page,blog_post_tag}.py
        ├── api/                # posts.json
        └── templates/blog/ (+ blocks/)
```

## Conventions

- One model per file inside each app's `models/` folder, re-exported in `models/__init__.py`.
- API code lives in each app's `api/` folder; templates in each app's `templates/<app>/` folder.
- Everything (code, UI text, docs) is in English.

## Page tree

```
Home
├── About me   (AboutPage)
├── Resume     (ResumePage)
└── Blog       (BlogIndexPage)
    └── Posts  (BlogPostPage)
```

## Post content

Post bodies are a StreamField with these blocks:

| Block | Use |
|---|---|
| Markdown | Markdown (tables, fenced code, images, GIFs, links); sanitized with bleach. YouTube/Vimeo `<iframe>` embeds are allowed. |
| Rich text | Wagtail editor |
| Image / GIF | Upload via the image library; GIFs keep their animation |
| Video / media link | oEmbed URL (YouTube, Vimeo, SoundCloud, Spotify, ...) |
| Video file | mp4/webm uploaded as a document |
| Code, Quote, Link, Raw HTML | Misc |

## Local workflow

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_content      # creates Home, About, Resume, Blog and a sample post
python manage.py createsuperuser
python manage.py runserver         # edit at http://localhost:8000/admin/
```

## Static build and GitHub Pages

GitHub Pages only serves static files, so the Wagtail admin runs locally and the site is exported:

```bash
SITE_BASE_PATH=<repo-name> python manage.py build_site   # output in build/
```

- `build_site` runs `collectstatic` and `wagtail-bakery`'s `build`, then prefixes root-relative URLs with `SITE_BASE_PATH` (leave empty for a user/organization site or custom domain).
- The API is exported as static JSON: `api/site.json`, `api/about.json`, `api/resume.json`, `api/posts.json`.
- Deploy: commit `db.sqlite3` and `media/`, push to `main`, and enable **Settings > Pages > Source: GitHub Actions**. `.github/workflows/deploy.yml` builds and publishes `build/`.
- Not available on a static site: server-side search and forms. oEmbed links are resolved at build time, so the build needs internet access when a post uses them.
- Set `DJANGO_SECRET_KEY` for any non-local use.
