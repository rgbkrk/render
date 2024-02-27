from typing import Any, Literal, Type, TypeVar
from typing_extensions import TypeGuard
from functools import wraps

from spork.protocols import HTMLRepresentable, MarkdownRepresentable


def is_html_representable(obj: Any) -> TypeGuard[HTMLRepresentable]:
    return hasattr(obj, "to_html") and callable(obj.to_html)


def is_markdown_representable(obj: Any) -> TypeGuard[MarkdownRepresentable]:
    return hasattr(obj, "to_markdown") and callable(obj.to_markdown)


T = TypeVar("T")


def renderable(cls: Type[T], default: Literal["markdown", "html"] = "html") -> Type[T]:
    """Decorate a class to make `render` functions the way to display in IPython"""

    def _repr_mimebundle_(self, include=None, exclude=None):
        # Allow the user to pass back a string of HTML, a VDOM object, or other displayable
        rendered = self.render()

        if isinstance(rendered, str):
            if default == "html":
                return {"text/html": rendered}
            else:
                return {"text/markdown": rendered}
        elif is_markdown_representable(rendered):
            return {"text/markdown": rendered.to_markdown()}
        elif is_html_representable(rendered):
            return {"text/html": rendered.to_html()}
        else:
            from IPython import get_ipython  # type: ignore

            ip = get_ipython()
            if ip is None or ip.display_formatter is None:
                raise ValueError("render() must return a string or a VDOM object")
            format = ip.display_formatter.format(rendered)  # type: ignore
            return format

        raise ValueError("render() must return something displayable")

    setattr(cls, "_repr_mimebundle_", _repr_mimebundle_)

    # WISH: I wish the resulting type could be something like `Type[T & Displayable]`
    return cls


def markdown(cls: Type[T]) -> Type[T]:
    """Decorate a class to make `render` functions return rendered Markdown in Jupyter"""
    return renderable(cls, default="markdown")


def html(cls: Type[T]) -> Type[T]:
    """Decorate a class to make `render` functions return rendered HTML in Jupyter"""
    return renderable(cls, default="html")


def auto_update(cls):
    """Decorate a class to make it automatically update when its attributes are set."""
    original_setattr = cls.__setattr__

    @wraps(original_setattr)
    def __setattr__(self, name, value):
        original_setattr(self, name, value)

        if hasattr(self, "update") and name != "display_id":
            self.update()

    cls.__setattr__ = __setattr__
    return cls
