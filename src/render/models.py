from pydantic import BaseModel, Field
from abc import ABC, abstractmethod
from IPython.display import display
import uuid

# TODO: Detect when running in a regular Python environment and use terminal rendering
#       instead of HTML and swap using `display_id` for \r
class ViewModel(ABC, BaseModel):
    display_id: str = Field(default_factory=lambda: str(uuid.uuid4()), exclude=True)

    def display(self):
        display(self, display_id=self.display_id)

    def update(self):
        display(self, update=True, display_id=self.display_id)
        return self

    @abstractmethod
    def render(self):
        """
        Abstract method for rendering. Subclasses should implement this.

        You can return a string of HTML or a VDOM object (see `vdom` package).
        """
        pass

    def _repr_html_(self):
        # Allow the user to pass back a string of HTML or a VDOM object
        rendered = self.render()

        if isinstance(rendered, str):
            return rendered
        elif hasattr(rendered, "to_html"):
            return rendered.to_html()

        raise ValueError("render() must return a string or a VDOM object")


class AutoViewModel(ViewModel):
    def __setattr__(self, name, value):
        super().__setattr__(name, value)
        if name != "display_id":
            self.update()
