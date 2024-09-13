from pyguiadapter.adapter import GUIAdapter


def str_example(str_arg1: str, str_arg2: str, str_arg3: str):
    pass


if __name__ == "__main__":
    adapter = GUIAdapter()
    adapter.add(str_example)
    adapter.run()
