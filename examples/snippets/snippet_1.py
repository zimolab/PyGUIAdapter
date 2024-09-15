from pyguiadapter.adapter import GUIAdapter


def f1(a: str, b: int, c: float):
    pass


def f2(a=10, b=0.5, c="hello", e=True, f=(1, 2, 3)):
    pass


def f3(a, b, c):
    """
    这是一个示例函数.

    Args:
        a (int): 参数a的描述.
        b (str): 参数b的描述.
        c (list): 参数c的描述.

    Returns:
        bool: 函数返回的结果描述.
    """
    pass


adapter = GUIAdapter()
adapter.add(f1)
adapter.add(f2)
adapter.add(f3)
adapter.run()
