from pathlib import Path
from bs4 import BeautifulSoup


def create_or_wrap(soup, class_name, soup_doc):
    """
    Wrap `soup` in a <div class="{class_name}"> if not already.
    Returns a tag ready to insert.
    """
    if soup.name == "div" and class_name in soup.get("class", []):
        return soup
    wrapper = soup_doc.new_tag("div", **{"class": class_name})
    wrapper.append(soup)
    return wrapper


def get_title(soup):
    # Determine title: first h1 > h2 > h3 > ...
    for level in range(1, 7):
        header = soup.find(f"h{level}")
        if header:
            return header.get_text().strip()
    return None


def parse_file(html_path):
    html_path = Path(html_path)
    with html_path.open("r", encoding="utf-8") as f:
        content = f.read()
    return BeautifulSoup(content, "html.parser")


def create_html_head(
    website_title="My Site", stylesheet_href="style.css", favicon_href="favicon.ico"
):
    """Return a <head> BeautifulSoup object for an HTML page."""
    soup = BeautifulSoup("", "html.parser")

    head = soup.new_tag("head")

    # Meta charset
    meta_charset = soup.new_tag("meta", charset="utf-8")
    head.append(meta_charset)

    # Viewport meta tag (important for mobile layout)
    meta_viewport = soup.new_tag("meta")
    meta_viewport.attrs["name"] = "viewport"
    meta_viewport.attrs["content"] = "width=device-width, initial-scale=1"
    head.append(meta_viewport)

    # Title
    title_tag = soup.new_tag("title")
    title_tag.string = website_title
    head.append(title_tag)

    # Stylesheet
    link_tag = soup.new_tag("link", rel="stylesheet", href=stylesheet_href)
    head.append(link_tag)

    # Favicon (optional)
    if favicon_href:
        favicon_tag = soup.new_tag(
            "link", rel="icon", href=favicon_href, type="image/x-icon"
        )
        head.append(favicon_tag)

    return head


def create_footer():
    soup = BeautifulSoup("", "html.parser")
    footer = soup.new_tag("div", **{"class": "footer"})
    return footer


def add_class(tag, class_name):
    """Add a class to a BeautifulSoup tag without overwriting existing classes."""
    if "class" in tag.attrs:
        if class_name not in tag["class"]:
            tag["class"].append(class_name)
    else:
        tag["class"] = [class_name]
