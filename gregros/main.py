import dis
from jinja2 import Environment, FileSystemLoader
from urllib.parse import quote, urlencode, urlparse, urlunparse

from gregros.topic import Topics

from .topics import (
    exported,
)


def run():
    topics = {k: v for k, v in locals().items() if k.startswith("")}
    env = Environment(loader=FileSystemLoader("."))

    # Make the function accessible in the template

    template = env.get_template("README.md.j2")
    output = template.render(
        exported=exported,
        **exported["cat"],
    )

    with open("README.md", "w", encoding="utf8") as f:
        f.write(output)
