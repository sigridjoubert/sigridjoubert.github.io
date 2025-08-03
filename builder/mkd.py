import mistune

from bs4 import BeautifulSoup

from .soup import get_title


def get_content(markdown_path):
    # Read the markdown file
    with open(markdown_path, "r", encoding="utf-8") as f:
        md_text = f.read()

    # Create a mistune Markdown parser with common plugins
    markdown = mistune.create_markdown(
        plugins=[
            "strikethrough",
            "table",
            "url",
            "footnotes",
            "def_list",
            "superscript",
            "subscript",
            "math",
        ]
    )

    # Convert to HTML
    html = markdown(md_text)

    # Parse HTML with BeautifulSoup
    soup = BeautifulSoup(html, "html.parser")

    return soup, get_title(soup)
