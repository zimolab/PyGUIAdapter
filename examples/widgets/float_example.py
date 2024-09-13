from pyguiadapter.adapter import GUIAdapter


def float_example(float_arg1: float, float_arg2: float, float_arg3: float):
    pass


if __name__ == "__main__":
    adapter = GUIAdapter()
    adapter.add(float_example)
    adapter.run()
