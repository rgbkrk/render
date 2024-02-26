from typing import Callable, Union, Protocol, Any, TypeGuard
from functools import wraps

from spork.protocols import HTMLRepresentable, MarkdownRepresentable

def is_html_representable(obj: Any) -> TypeGuard[HTMLRepresentable]:
    return hasattr(obj, "to_html") and callable(obj.to_html)

def is_markdown_representable(obj: Any) -> TypeGuard[MarkdownRepresentable]:
    return hasattr(obj, "to_markdown") and callable(obj.to_markdown)

def view(cls):
    """Decorate a class to make `render` functions the way to display in IPython"""
    def _repr_mimebundle_(self, include=None, exclude=None):
        # Allow the user to pass back a string of HTML, a VDOM object, or other displayable
        rendered = self.render()

        if isinstance(rendered, str):
            return {"text/html": rendered}
        elif is_markdown_representable(rendered):
            return {"text/markdown": rendered.to_markdown()}
        elif is_html_representable(rendered):
            return {"text/html": rendered.to_html()}
        else:
            from IPython import get_ipython # type: ignore
            ip = get_ipython()
            if ip is None or ip.display_formatter is None:
                raise ValueError("render() must return a string or a VDOM object")
            format = ip.display_formatter.format(rendered) # type: ignore
            return format

        raise ValueError("render() must return something displayable")
    cls._repr_mimebundle_ = _repr_mimebundle_
    return cls


def auto_update(cls):
    original_setattr = cls.__setattr__

    @wraps(original_setattr)
    def __setattr__(self, name, value):
        original_setattr(self, name, value)

        if hasattr(self, 'update') and name != "display_id":
            self.update()

    cls.__setattr__ = __setattr__
    return cls
