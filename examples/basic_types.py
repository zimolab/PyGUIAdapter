from pyguiadapter.adapter import GUIAdapter


def basic_types(
    int_arg: int,
    bool_arg: bool,
    float_arg: float,
    str_arg: str,
    list_arg: list,
    tuple_arg: tuple,
    dict_arg: dict,
):
    pass


if __name__ == "__main__":
    adapter = GUIAdapter()
    adapter.add(basic_types)
    adapter.run()
