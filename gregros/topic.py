import itertools
from urllib.parse import urlencode

url_base = "https://github.com/GregRos"


class Topic:
    def __init__(
        self,
        name: str,
        is_negated: bool = False,
        display: str | None = None,
    ):
        self.name = name
        self.is_negated = is_negated
        self.display_name = display or name.title()

    def __invert__(self):
        return Topic(self.name, is_negated=not self.is_negated)

    def __str__(self):
        return f"{"-" if self.is_negated else ""}topic:{self.name}"

    def __neg__(self):
        return Topic(self.name, is_negated=True)

    def __sub__(self, other: "Topic | Topics") -> "Topics":
        return Topics(self) + -other

    def __add__(self, other: "Topic | Topics") -> "Topics":
        return Topics(self) + other


class Topics:
    def __init__(self, *topics: "Topic | Topics"):
        self._topics = tuple(
            itertools.chain.from_iterable(
                [
                    topic._topics if isinstance(topic, Topics) else [topic]
                    for topic in topics
                ]
            )
        )

    def __add__(self, other):
        if isinstance(other, Topic):
            return Topics(*self._topics, other)
        elif isinstance(other, Topics):
            return Topics(*self._topics, *other._topics)
        else:
            raise TypeError(f"Unsupported type for addition: {type(other)}")

    def __invert__(self):
        return Topics(*[~topic for topic in self._topics])

    def __neg__(self):
        return Topics(*[~topic for topic in self._topics])

    def __sub__(self, other: "Topic | Topics"):
        return self + -other

    def to_display(self) -> str:
        return self._topics[0].display_name if self._topics else ""

    def to_query(self):
        query = urlencode(
            {
                "tab": "repositories",
                "q": " ".join(str(t) for t in self._topics),
            }
        )
        return query

    def to_url(self) -> str:
        return f"{url_base}?{self.to_query()}"
