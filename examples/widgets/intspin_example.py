from pyguiadapter.adapter import GUIAdapter


def intspin_example(int_arg1: int, int_arg2: int, int_arg3: int):
    pass


if __name__ == "__main__":
    adapter = GUIAdapter()
    adapter.add(intspin_example)
    adapter.run()
