import tinycss2
from .logger import get_logger

LOGGER = get_logger()


def parse_declarations(declaration_list):
    """Convert a list of declarations to a name-value dictionary."""
    declarations = tinycss2.parse_declaration_list(declaration_list)
    result = {}
    for decl in declarations:
        if decl.type == "declaration" and not decl.name.startswith("--"):
            result[decl.name] = tinycss2.serialize(decl.value).strip()
    return result


def css_to_dict(css_text):
    """Parse CSS into a nested dictionary structure."""
    rules = tinycss2.parse_stylesheet(
        css_text, skip_whitespace=True, skip_comments=True
    )
    style_dict = {}

    for rule in rules:
        if rule.type == "qualified-rule":
            selector = tinycss2.serialize(rule.prelude).strip()
            style_dict[selector] = parse_declarations(rule.content)

        elif rule.type == "at-rule" and rule.content:
            at_name = f"@{rule.at_keyword} {tinycss2.serialize(rule.prelude).strip()}"
            nested_rules = tinycss2.parse_rule_list(rule.content)
            style_dict[at_name] = {}
            for nested in nested_rules:
                if nested.type == "qualified-rule":
                    selector = tinycss2.serialize(nested.prelude).strip()
                    style_dict[at_name][selector] = parse_declarations(nested.content)

    return style_dict


def dict_to_css(style_dict):
    """Convert the nested dictionary back into CSS."""
    css_lines = []

    for selector, props in style_dict.items():
        if not selector.startswith("@"):
            block = f"{selector} {{\n"
            for name, value in props.items():
                block += f"  {name}: {value};\n"
            block += "}"
            css_lines.append(block)
        else:
            # Handle @media and similar
            block = f"{selector} {{\n"
            for inner_selector, inner_props in props.items():
                block += f"  {inner_selector} {{\n"
                for name, value in inner_props.items():
                    block += f"    {name}: {value};\n"
                block += "  }\n"
            block += "}"
            css_lines.append(block)

    return "\n\n".join(css_lines)


class Stylesheet:

    def __init__(self, css_text=None, path=None):
        """Initialize from CSS text or a file path."""
        if css_text:
            LOGGER.info("Stylesheet object initialized from text.")
            self.rules = css_to_dict(css_text)
        elif path:
            with open(path, encoding="utf-8") as f:
                self.rules = css_to_dict(f.read())
            LOGGER.info(f"Stylesheet object initialized form {path}.")
        else:
            LOGGER.info(f"Empty stylesheet object initialized.")
            self.rules = {}

    def write(self, path):
        """Write the current stylesheet to a file."""
        css_text = dict_to_css(self.rules)
        LOGGER.info(f"Stylesheet object written to {path}.")
        with open(path, "w", encoding="utf-8") as f:
            f.write(css_text)

    def add_element(self, selector, declarations, at_rule=None):
        """
        Add or update a CSS rule.

        - `selector`: str, like "h1" or ".my-class"
        - `declarations`: dict of CSS properties and values, like {"color": "red"}
        - `at_rule`: optional str, like "@media screen and (max-width: 600px)"
        """
        if at_rule:
            if at_rule not in self.rules:
                self.rules[at_rule] = {}
            self.rules[at_rule][selector] = declarations
        else:
            self.rules[selector] = declarations

    def __getitem__(self, selector):
        return self.rules[selector]
