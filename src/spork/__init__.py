# SPDX-FileCopyrightText: 2024-present Kyle Kelley <rgbkrk@gmail.com>
#
# SPDX-License-Identifier: MIT

from .models import View, AutoUpdate, __doc__
from .decorators import renderable, auto_update, markdown, html

# Use the doc from the models setup
__doc__ = __doc__


@markdown
class Markdown(AutoUpdate):
    """An autoupdating markdown class.

    This class provides an easy way to create and update a Markdown string in Jupyter Notebooks. It
    supports real-time updates of Markdown content which is useful for emitting Large Language
    Model output as it is generated.

    >>> m = Markdown()
    >>> m.display()
    This will come out...

    >>> for i in "This will come out one character at a time":
    ...     m.append(i)

    """

    content: str

    def render(self):
        return self.content

    def append(self, content: str):
        self.content += content


__all__ = [
    "View",
    "AutoUpdate",
    "renderable",
    "auto_update",
    "markdown",
    "html",
    "Markdown",
]
