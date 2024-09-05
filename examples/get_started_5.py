from pyguiadapter.adapter import GUIAdapter


def bar_func(a: int, b: str, c: float = 5.0 - 1):
    """
    @params
    [a]
    default_value = 100

    [b]
    default_value = "hello world"

    @end
    """
    pass


if __name__ == "__main__":
    adapter = GUIAdapter()
    adapter.add(bar_func)
    adapter.run()
