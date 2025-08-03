import shutil

from .page import Page
from .site import Site
from .css import Stylesheet
from .soup import parse_file, get_title
from .paths import (
    ASSETS_DIR,
    CUSTOM_DIR,
    PAGES_DIR,
    BUILD_DIR,
    JS_DIR,
    STYLE_FILE,
    ICON_FILE,
    FONTS_DIR,
)
from .logger import get_logger
from .img import convert_and_resize_to_webp

LOGGER = get_logger()


class Builder:

    def __init__(self, site_name):
        self.content = {}
        self.custom_pages = []
        self.site = Site.get(name=site_name)
        self.stylesheet = Stylesheet(path=STYLE_FILE)

    def get_content(self):
        # First get index pages and other custom html pages
        for f in CUSTOM_DIR.rglob("*"):
            if f.suffix == (".html"):
                content = parse_file(f)
                title = "index" if f.stem == "index" else get_title(content)
                title = title if title else Site._name
                page = Page(content=content, title=title)
                page.set_path(f.relative_to(CUSTOM_DIR))
                self.custom_pages.append(page)

        for path in sorted(PAGES_DIR.iterdir(), key=lambda p: (p.is_dir(), p.name)):
            # Iterate through files before folders
            if path.is_file():
                page = Page(mkd_path=str(path))
                self.content[page.title] = page
            if path.is_dir():
                dirname = path.name
                if dirname not in self.content:
                    self.content[dirname] = {}
                for p in path.iterdir():
                    if p.is_file():
                        page = Page(mkd_path=str(p))
                        self.content[dirname][page.title] = page

    def move_js_content(self):
        try:
            shutil.copytree(JS_DIR, BUILD_DIR / "js")
        except FileNotFoundError as e:
            LOGGER.error(f"Javascript folder {JS_DIR} empty or missing.")

    def write_stylesheet(self):
        # self.stylesheet.write(BUILD_DIR / "style.css")
        shutil.copy2(STYLE_FILE, BUILD_DIR / "style.css")

    def move_icon(self):
        shutil.copy2(ICON_FILE, BUILD_DIR / ICON_FILE.name)

    def format_assets(self):
        for f in (ASSETS_DIR / "img").rglob("*"):
            convert_and_resize_to_webp(f)

    def move_assets(self):
        shutil.copytree(ASSETS_DIR, BUILD_DIR / "assets")

    def build_site(self):
        try:
            shutil.rmtree(BUILD_DIR, ignore_errors=True)
            BUILD_DIR.mkdir(parents=True, exist_ok=True)
            self.get_content()
            self.site.build_from_dict(self.content)
            for page in self.custom_pages:
                self.site.add_page(page)
            self.format_assets()
            self.site.format_content()
            self.move_js_content()
            self.move_icon()
            self.move_assets()
            self.site.write_content()
            self.write_stylesheet()
        except Exception as e:
            raise (e)
