# Django Wagtail Blog

A personal site built with [Wagtail](https://wagtail.org): an **About me** page (contact information), a **Resume** page and a **Blog**. The Wagtail admin runs locally and the site is exported as static HTML for GitHub Pages.

See [contrib/structure/README.md](contrib/structure/README.md) for the project layout.

## Requirements

- Python 3.11+ (tested with 3.13)
- Git

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_content    # creates Home, About, Resume, Blog and a sample post
python manage.py createsuperuser
python manage.py runserver
```

- Site: http://localhost:8000/
- Admin: http://localhost:8000/admin/

`seed_content` only runs when no home page exists, so it is safe to run again.

## Configure

| Setting | Where | Description |
|---|---|---|
| `SITE_NAME` | `config/settings.py` | Name shown in the header, footer and page titles |
| `DJANGO_SECRET_KEY` | environment variable | Secret key. Set it for anything other than local use |
| `DJANGO_DEBUG` | environment variable | `1` (default) or `0` |
| `SITE_BASE_PATH` | environment variable | Sub-path used when building, normally the repository name. Leave empty for a `<user>.github.io` repository or a custom domain |
| `WAGTAILADMIN_BASE_URL` | `config/settings.py` | Base URL used by the admin |

Also change the sample content (name, e-mail, GitHub link) in the admin after seeding.

## Add content

Log in to `/admin/` and use **Pages**. The page tree is:

```
Home
├── About me
├── Resume
└── Blog
    └── Posts
```

### About me (contact information)

Open **About me** and edit the headline, photo, bio, e-mail, phone and location. Use **Contact link** to add links such as GitHub, LinkedIn or X.

### Resume

Open **Resume** and edit the summary. Add **Experience**, **Education** and **Skill** entries (they can be reordered). Optionally attach a PDF to show a "Download PDF" button. Leave the end date of an experience empty if it is your current job.

### Blog posts

1. Open **Blog**, click **Add child page** and choose **Blog post page**.
2. Fill in the title, date, tags, intro and cover image.
3. Build the body from these blocks:

| Block | Use |
|---|---|
| Markdown | Markdown text with headings, lists, tables, code fences, links and images |
| Rich text | The Wagtail visual editor |
| Image / GIF | Upload through the image library. GIFs keep their animation |
| Video / media link | Paste a YouTube, Vimeo, SoundCloud, Spotify or other oEmbed URL |
| Video file | An mp4/webm uploaded in **Documents** |
| Code, Quote, Link, Raw HTML | Other content |

4. Click **Publish**.

Markdown examples:

```markdown
![Alt text](https://example.com/picture.gif)
[Link text](https://example.com)
<iframe src="https://www.youtube.com/embed/VIDEO_ID" width="560" height="315" allowfullscreen></iframe>
```

Markdown is sanitized. Only YouTube and Vimeo iframes are kept, and scripts are removed. Use the **Raw HTML** block for anything else.

Images and documents uploaded in the admin are stored in `media/`.

## Build the static site

```bash
SITE_BASE_PATH=<repo-name> python manage.py build_site
```

The result is in `build/`. It includes the HTML pages, `static/`, `404.html` and a static JSON API:

- `api/site.json`
- `api/about.json`
- `api/resume.json`
- `api/posts.json`

To preview it locally (the sub-path is not applied without `SITE_BASE_PATH`):

```bash
python manage.py build_site
python -m http.server 8080 --directory build
```

Server-side search and forms do not work on a static site. oEmbed links are resolved during the build, so it needs internet access.

## Deploy to GitHub Pages

1. In the repository, go to **Settings > Pages** and set **Source** to **GitHub Actions**.
2. Commit your content: `db.sqlite3` and `media/`. The workflow builds the site from them.
3. Push to `main`.

`.github/workflows/deploy.yml` installs the dependencies, runs the migrations and `build_site` (with `SITE_BASE_PATH` set to the repository name) and publishes `build/`. The site will be at `https://<user>.github.io/<repo-name>/`.

Workflow for each update: edit in the admin locally, commit `db.sqlite3` and `media/`, push.

The admin is not published. Anyone with the repository can read `db.sqlite3`, so do not store private data in the content.

## Troubleshooting

- `No module named 'pkg_resources'`: `django-bakery` needs `setuptools<81`. Run `pip install -r requirements.txt`.
- Broken links or CSS after deploy: check that `SITE_BASE_PATH` matches the repository name.
- A page is missing from the build: make sure it is published (not a draft).
