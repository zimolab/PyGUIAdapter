from pyguiadapter.adapter import GUIAdapter


def bool_example(bool_arg1: bool, bool_arg2: bool, bool_arg3: bool):
    pass


if __name__ == "__main__":
    adapter = GUIAdapter()
    adapter.add(bool_example)
    adapter.run()
