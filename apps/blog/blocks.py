import bleach
import markdown
from django.utils.safestring import mark_safe
from wagtail import blocks
from wagtail.documents.blocks import DocumentChooserBlock
from wagtail.embeds.blocks import EmbedBlock
from wagtail.images.blocks import ImageChooserBlock

ALLOWED_TAGS = frozenset(bleach.sanitizer.ALLOWED_TAGS) | {
    "p", "pre", "br", "hr", "img", "h1", "h2", "h3", "h4", "h5", "h6",
    "table", "thead", "tbody", "tr", "th", "td", "span", "div", "sup", "sub",
    "video", "source", "iframe",
}
ALLOWED_ATTRIBUTES = {
    "*": ["class", "id"],
    "a": ["href", "title", "rel", "target"],
    "img": ["src", "alt", "title", "width", "height", "loading"],
    "video": ["src", "controls", "poster", "width", "height", "loop", "muted"],
    "source": ["src", "type"],
    "iframe": ["src", "width", "height", "allowfullscreen", "title", "loading"],
}
ALLOWED_IFRAME_HOSTS = (
    "https://www.youtube.com/embed/",
    "https://www.youtube-nocookie.com/embed/",
    "https://player.vimeo.com/video/",
)


def _allow_attribute(tag, name, value):
    if tag == "iframe" and name == "src":
        return value.startswith(ALLOWED_IFRAME_HOSTS)
    return name in ALLOWED_ATTRIBUTES.get(tag, []) or name in ALLOWED_ATTRIBUTES["*"]


def render_markdown(text):
    html = markdown.markdown(
        text, extensions=["extra", "fenced_code", "tables", "sane_lists", "toc"]
    )
    cleaned = bleach.clean(
        html, tags=ALLOWED_TAGS, attributes=_allow_attribute, protocols=["http", "https", "mailto"]
    )
    return mark_safe(cleaned)


class MarkdownBlock(blocks.TextBlock):
    def __init__(self, **kwargs):
        kwargs.setdefault("rows", 14)
        kwargs.setdefault(
            "help_text",
            "Markdown. Images, GIFs and links work with ![alt](url) and [text](url). "
            "Videos: use the Video embed block or an <iframe> from YouTube/Vimeo.",
        )
        super().__init__(**kwargs)

    def render_basic(self, value, context=None):
        return render_markdown(value or "")

    class Meta:
        icon = "doc-full"
        label = "Markdown"


class MediaImageBlock(blocks.StructBlock):
    image = ImageChooserBlock()
    caption = blocks.CharBlock(required=False)

    class Meta:
        icon = "image"
        label = "Image / GIF"
        template = "blog/blocks/image_block.html"


class VideoFileBlock(blocks.StructBlock):
    file = DocumentChooserBlock(help_text="mp4 / webm uploaded as a document.")
    caption = blocks.CharBlock(required=False)

    class Meta:
        icon = "media"
        label = "Video file"
        template = "blog/blocks/video_file_block.html"


class PostBodyBlock(blocks.StreamBlock):
    markdown = MarkdownBlock()
    rich_text = blocks.RichTextBlock()
    image = MediaImageBlock()
    video_embed = EmbedBlock(
        icon="media",
        label="Video / media link",
        help_text="YouTube, Vimeo, SoundCloud, Spotify, Twitter and other oEmbed links.",
    )
    video_file = VideoFileBlock()
    code = blocks.StructBlock(
        [
            ("language", blocks.CharBlock(required=False)),
            ("code", blocks.TextBlock()),
        ],
        icon="code",
        template="blog/blocks/code_block.html",
    )
    quote = blocks.BlockQuoteBlock()
    link = blocks.URLBlock(icon="link")
    html = blocks.RawHTMLBlock(icon="code", label="Raw HTML")
