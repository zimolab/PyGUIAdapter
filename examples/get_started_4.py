from pyguiadapter.adapter import GUIAdapter


def foo_func(a: int, b: str, c: float):
    """
    foo_func
    @param a: description for param <b>a</b>
    @param b: description for param <b>b</b>
    @param c: description for param <b>c</b>
    @return:
    """
    pass


if __name__ == "__main__":
    adapter = GUIAdapter()
    adapter.add(foo_func)
    adapter.run()
