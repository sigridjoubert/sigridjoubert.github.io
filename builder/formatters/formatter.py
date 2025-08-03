from bs4 import BeautifulSoup
import hashlib
import base64

from ..soup import add_class


def short_hash(text):
    h = hashlib.md5(text.encode()).digest()
    return base64.urlsafe_b64encode(h).decode()[:11]  # shorter & URL-safe


class Formatter:
    """
    Base class for formatting html content.
    only find() and edit() need their behaviour chhanged when inheriting.
    """

    def __init__(self):
        pass

    def class_hash(self):
        return short_hash(str(self.__class__))

    def mark_tag(self, tag):
        add_class(tag, self.class_hash())

    def is_unmarked(self, tag):
        return self.class_hash() not in tag.get("class", [])

    def format_content(self, soup):
        raise NotImplementedError("'Tis but a baseclass.")
