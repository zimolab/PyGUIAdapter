from pyguiadapter.adapter import GUIAdapter


def foo(a: int = -100, b: int = 1 + 1):
    """
    @param a: this is parameter a
    @param b: this is parameter b
    @return:
    """


adapter = GUIAdapter()
adapter.add(foo)
adapter.run()
