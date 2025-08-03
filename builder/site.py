from pathlib import Path

from .menu import Menu
from .paths import ASSETS_DIR, PAGES_DIR, BUILD_DIR, STYLE_FILE, ICON_FILE
from .soup import create_html_head, create_footer
from .page import Page
from .logger import get_logger

LOGGER = get_logger()


class Site:

    _instance = None
    _name = None

    @classmethod
    def get(cls, name):
        cls._name = name
        if cls._instance is None:
            return cls()
        return cls._instance

    def __init__(self):
        self.pages = []
        self.menu = Menu(self.__class__._name)
        self.head = create_html_head(
            website_title=self.__class__._name,
            stylesheet_href=Path("/style.css"),
            favicon_href=ICON_FILE,
        )
        self.footer = create_footer()

    def gen_page_path(self, page, category=None):
        if category:
            return Path(category) / self.__class__.gen_page_filename(page)
        return Path(self.__class__.gen_page_filename(page))

    @classmethod
    def gen_page_filename(cls, page):
        return (
            page.title.strip()
            .lower()
            .replace(" ", "_")
            .replace("/", "-")
            .replace("\\", "-")
            + ".html"
        )

    def build_from_dict(self, content):
        def rec_build_menu(c, cat=None):
            for k, v in c.items():
                if isinstance(v, Page):
                    v.set_path(self.gen_page_path(v, cat))
                    if cat:
                        if cat != "pages":
                            self.menu.add_subpage(cat, k, v)
                    else:
                        self.menu.add_page(k, v)
                    self.pages.append(v)
                else:
                    self.menu.add_category(k)
                    rec_build_menu(v, k)

        rec_build_menu(content, None)

    def write_content(self):
        for page in self.pages:
            page.assemble(self.menu, self.head, self.footer)
            page.write()

    def add_page(self, page):
        LOGGER.info(f"Page {page.title} added to site.")
        self.pages.append(page)

    def format_content(self):
        for page in self.pages:
            page.format_content()
