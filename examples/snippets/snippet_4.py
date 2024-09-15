from pyguiadapter.adapter import GUIAdapter
from pyguiadapter.widgets import (
    IntSpinBoxConfig,
    SliderConfig,
    TextEditConfig,
)


def foo(a: int, b: int, c: str = "hello world!"):
    pass


def foo2(a: int, b: int, c: str = "hello world!"):
    pass


foo_configs = {
    "a": IntSpinBoxConfig(
        default_value=1,
        min_value=0,
        max_value=10,
        step=1,
        label="a",
        description="parameter a",
    ),
    "b": SliderConfig(
        default_value=50,
        min_value=0,
        max_value=100,
        label="b",
        description="parameter b",
    ),
    "c": TextEditConfig(
        default_value="Hello PyGUIAdapter!",
        label="c",
        description="parameter c",
    ),
}

foo2_configs = {
    "a": {
        "default_value": 1,
        "min_value": 0,
        "max_value": 10,
        "step": 1,
        "label": "a",
        "description": "parameter a",
    },
    "b": {
        "default_value": 50,
        "min_value": 0,
        "max_value": 100,
        "label": "b",
        "description": "parameter b",
    },
    "c": {
        "default_value": "Hello PyGUIAdapter!",
        "label": "c",
        "description": "parameter c",
    },
}


adapter = GUIAdapter()
adapter.add(foo, widget_configs=foo_configs)
adapter.add(foo2, widget_configs=foo2_configs)
adapter.run()
