from pyguiadapter.adapter import GUIAdapter


def foo(a: int, b: int) -> float:
    return float(a) / b


if __name__ == "__main__":
    adapter = GUIAdapter()
    adapter.add(foo)
    adapter.run()
