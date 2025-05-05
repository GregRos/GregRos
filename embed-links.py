import os
import re
from collections import OrderedDict


def to_topic_criterion(topic: str) -> str:
    if topic.startswith("-"):
        return f"-topic:{topic[1:]}"
    return f"topic:{topic}"


def splat_query(*topics: str) -> str:
    """
    Splits a list of topics into a query string for GitHub search.
    """

    return "+".join([to_topic_criterion(topic) for topic in topics if topic])


main_types = {"typescript", "library", "framework"}


def replace_custom_links(md_text):
    # Match [<kind|label>] pattern
    pattern = re.compile(r"\[(.+?)\]\[(.+?),(.+?)\]")
    link_defs = OrderedDict()

    def replacer(match):
        text, kind, label = match.group(1), match.group(2), match.group(3)
        label = "kubernetes" if label == "k8s" else label  # special casing
        display = label if label != "dotnet" else ".NET"  # special casing

        # Store the actual URL
        if kind == "category":
            if label == "packages":
                query = "topic:package"
            elif label == "incomplete":
                query = splat_query("incomplete", "package", "-obsolete")
            else:
                query = splat_query(label)
        elif kind == "type" or kind == "lang":
            query = splat_query(
                label,
                *(
                    ["-obsolete", "-incomplete", "package"]
                    if label in main_types
                    else []
                ),
            )
        elif kind == "tech" or kind == "domain":
            query = splat_query(label, "-obsolete")
        else:
            query = splat_query(label)
        url = f"https://github.com/GregRos?tab=repositories&q={query}"
        result = f"[{text}]({url})"
        return result

    # Replace all
    new_md = pattern.sub(replacer, md_text)

    return new_md


script_dir = os.path.dirname(os.path.abspath(__file__))

# Example usage
if __name__ == "__main__":
    with open(f"{script_dir}/README.template.md", "r", encoding="utf-8") as f:
        content = f.read()
    updated = replace_custom_links(content)
    with open(f"{script_dir}/README.md", "w", encoding="utf-8") as f:
        f.write(updated)
