from pathlib import Path
from bs4 import BeautifulSoup
from .logger import get_logger

LOGGER = get_logger()


class Menu:
    def __init__(self, title):
        self.soup = BeautifulSoup("", "html.parser")
        self.container = self.soup.new_tag("nav", **{"class": "menu"})
        self.soup.append(self.container)
        self.categories = {}  # category_name -> submenu container

        # Init top menu button with link to index and site title
        link = self.soup.new_tag("a", href="/index.html", **{"class": "menutitle"})
        link.string = title
        self.container.append(link)

    def add_page(self, name, page):
        LOGGER.info(f"Page {name} added to menu")
        link = self.soup.new_tag(
            "a", href=Path("/") / page.path, **{"class": "menuelement"}
        )
        link.string = name
        self.container.append(link)

    def add_category(self, name):
        """Add a toggleable category using <input type='checkbox'> and <label>."""
        LOGGER.info(f"Added category {name} to menu.")
        safe_id = f"menu_toggle_{name.lower().replace(' ', '_')}"
        wrapper = self.soup.new_tag("div", **{"class": "menucategory"})

        # Hidden checkbox
        checkbox = self.soup.new_tag("input", type="checkbox", id=safe_id, hidden=True)
        wrapper.append(checkbox)

        # Clickable label that toggles the checkbox
        label = self.soup.new_tag("label", **{"for": safe_id, "class": "menuelement"})
        label.string = name
        wrapper.append(label)

        # Submenu container (shown when checkbox is checked)
        submenu = self.soup.new_tag("div", **{"class": "menusubcontainer"})
        wrapper.append(submenu)

        self.container.append(wrapper)
        self.categories[name] = submenu

    def add_subpage(self, category_name, subname, subpage):
        if category_name not in self.categories:
            raise ValueError(f"Category '{category_name}' not found.")
        LOGGER.info(
            f"Added page {subname} (link: {subpage.path}) to category {category_name} in Menu."
        )
        submenu = self.categories[category_name]
        link = self.soup.new_tag(
            "a", href=Path("/") / subpage.path, **{"class": "menusubelement"}
        )
        link.string = subname
        submenu.append(link)

    def get_soup(self):
        return self.soup
