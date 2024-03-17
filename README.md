# PyGUIAdapter

A GUI adapter for python functions. 

It is used to make gui for almost any python functions in just a few lines.

Turn your function(s) into gui is easy:

1. Import GUIAdapter from  pyguiadapter.adapter package
2. Write your functions
3. Create an instance of GUIAdapter
4. Add your function(s) to the instance
5. Invoke run() method of the instance

Simple example:

```python
from pyguiadapter.adapter import GUIAdapter

def user_function(a: int, b: int) -> int:
    """This is a user function."""
    return a + b


gui_adapter = GUIAdapter()
gui_adapter.add(user_function)
gui_adapter.run()
```

Check `examples/` for more examples.

Check `screenshots/` for the screenshot of the examples.


## Current Status

I spent almost a week of my spare time to create this library.

The code is not that fancy but it works. 

A lot of work is still to be done, including:

1. a stable api
2. i18n
3. more tests
4. more examples
5. more widget types
6. documentation
7. and so on

**Any help and suggestions are welcomed**

## Underlying...

GUIAdapter is built on top of `function2widgets`(also my own library which is based on PyQt6).
