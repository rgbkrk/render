# spork

[![PyPI - Version](https://img.shields.io/pypi/v/spork.svg)](https://pypi.org/project/spork)

[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/spork.svg)](https://pypi.org/project/spork)

Exposing simple ways to render pydantic models in notebooks and other interactive computing environments.

----

**Table of Contents**

- [Installation](#installation)
- [Background](#background)
- [License](#license)

----

## Installation

```console
pip install spork
```

## Background

I created this module because I wanted a simple way to describe how to render pydantic models, especially when streaming in data to update a model. Wouldn't it be nice to see a visual display of the model as it's being updated?

To explore this space a bit, I've created a `ViewModel` and an `AutoViewModel`. This lets you update fields and have them update within the notebook. 

## Usage

You can use existing pydantic models or create new ones by inheriting from `AutoViewModel`:

```python
from spork import AutoViewModel
from pydantic import BaseModel

class Record(BaseModel):
    name: str
    age: int

class RecordView(Record, AutoViewModel):
    def render(self):
        return f"<b>{self.name}</b> is {self.age} years old."


rv = RecordView(name="Kyle", age=35)
rv.display()
```

When using an `AutoViewModel`, you can update the fields and the view will update wherever you ran `.display()`

```python
rv.age = 101
```


## License

`spork` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
