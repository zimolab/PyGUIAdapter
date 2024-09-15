from pyguiadapter.adapter import GUIAdapter


def foo(a: int, b: int, c: str = "hello world!"):
    """
    @params
    [a]
    widget_class="IntSpinBox"
    default_value=1
    min_value=0
    max_value=10
    step=1
    label="a"
    description="parameter a"

    [b]
    widget_class="Slider"
    default_value=50
    min_value=0
    max_value=100
    label="b"
    description="parameter b"

    [c]
    widget_class="TextEdit"
    default_value="Hello PyGUIAdapter!"
    label="c"
    description="parameter c"
    @end
    """


def foo2(a: int, b: int, c: str = "hello world!"):
    """
    @params
    [a]
    default_value=1
    min_value=0
    max_value=10
    step=1
    label="a"
    description="parameter a"

    [b]
    default_value=50
    min_value=0
    max_value=100
    label="b"
    description="parameter b"

    [c]
    default_value="Hello PyGUIAdapter!"
    label="c"
    description="parameter c"
    @end
    """


adapter = GUIAdapter()
adapter.add(foo)
adapter.add(foo2)
adapter.run()
