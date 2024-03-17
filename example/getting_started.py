from pyguiadapter.interact import ulogging
from pyguiadapter.interact.uprint import uprint


class Foo(object):
    def __init__(
        self, a: int, b: float, c: str, d: bool, e: list[int], f: dict[str, int]
    ):
        pass

    def a(self, arg1: int, arg2: float):
        """
        这是一个函数
        :param arg1:
        :param arg2:
        :return:
        """
        msg = """
             再 别 康 桥
                徐志摩
        轻轻地我走了，正如我轻轻地来，
        我轻轻地挥一挥手，
        告别西天的云彩。
        """.rstrip()
        uprint(msg)
        ulogging.enable_timestamp(True)
        ulogging.debug("hello world", timestamp=True)
        ulogging.info("hello world")
        ulogging.warning("hello world")
        ulogging.critical("hello world")


if __name__ == "__main__":
    from pyguiadapter.adapter import GUIAdapter

    adapter = GUIAdapter()
    adapter.always_show_selection_window = False
    adapter.initialization_window_config.title = "初始化"

    with adapter.initialize_class(Foo) as foo:
        adapter.add(Foo.a, foo)
        adapter.run()
