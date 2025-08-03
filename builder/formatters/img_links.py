from pathlib import Path

from .formatter import Formatter
from ..paths import ASSETS_DIR


class ImageLinkFormatter(Formatter):

    def format_content(self, soup):
        for img in soup.find_all("img"):
            old_path = img["src"]
            new_path = Path("/") / "assets" / "img" / f"{Path(old_path).stem}.webp"
            img["src"] = new_path
        return soup
