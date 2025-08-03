from bs4 import BeautifulSoup

from .mkd import get_content
from .soup import create_or_wrap, get_title
from .paths import BUILD_DIR
from .formatters import FORMATTERS
from .logger import get_logger

LOGGER = get_logger()


class Page:

    def __init__(self, mkd_path=None, content=None, title=None):
        if mkd_path:
            self.content, self.title = get_content(mkd_path)
            LOGGER.info(f"Page {self.title} initialized using {mkd_path}.")
        elif content:
            self.content = content
            self.title = title if title else get_title(content)
            if not self.title:
                raise Error(
                    f"Cannot create page as no title could be extracted and none was passed.\nContent:\n{self.content.prettify()}"
                )
            LOGGER.info(f"Page {self.title} initialized fom content.")
        self.path = None

    def write(self):
        dest = BUILD_DIR / self.path
        dest.parent.mkdir(parents=True, exist_ok=True)
        with open(dest, "w", encoding="utf-8") as f:
            f.write(self.content.prettify())
        LOGGER.info(f"Writing page {self.title} to {self.path}.")

    def assemble(self, menu, head, footer):
        doc = BeautifulSoup(
            "<!DOCTYPE html><html><head></head><body></body></html>", "html.parser"
        )

        # Insert <head> content
        doc.head.append(head)

        # Insert body components, wrapped appropriately
        body = doc.body
        body.append(create_or_wrap(menu.container, "menu", doc))
        body.append(create_or_wrap(self.content, "content", doc))
        body.append(create_or_wrap(footer, "footer", doc))

        self.content = doc

    def set_path(self, path):
        LOGGER.info(f"Set path of page {self.title} to {path}.")
        self.path = path

    def format_content(self):
        for formatter in FORMATTERS:
            self.content = formatter.format_content(self.content)
