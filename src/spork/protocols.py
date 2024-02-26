from typing import Protocol

class HTMLRepresentable(Protocol):
    """Objects with a `to_html` method are displayable with ViewModels."""
    def to_html(self) -> str:
        ...

class MarkdownRepresentable(Protocol):
    """Objects with a `to_markdown` method are displayable with ViewModels."""
    def to_markdown(self) -> str:
        ...
