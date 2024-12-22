"""
@Time    : 2024.10.20
@File    : extend_types.py
@Author  : zimolab
@Project : PyGUIAdapter
@Desc    : 定义了一些语义化类型。
"""


# noinspection PyPep8Naming
class text_t(str):
    pass


# noinspection PyPep8Naming
class int_t(int):
    pass


# noinspection PyPep8Naming
class float_t(float):
    pass


# noinspection PyPep8Naming
class file_t(str):
    pass


# noinspection PyPep8Naming
class files_t(list):
    pass


# noinspection PyPep8Naming
class directory_t(str):
    pass


dir_t = directory_t


# noinspection PyPep8Naming
class choice_t(object):
    pass


# noinspection PyPep8Naming
class choices_t(list):
    pass


# noinspection PyPep8Naming
class int_slider_t(int):
    pass


# noinspection PyPep8Naming
class int_dial_t(int):
    pass


# noinspection PyPep8Naming
class color_t(object):
    pass


# noinspection PyPep8Naming
class color_tuple_t(tuple):
    pass


# noinspection PyPep8Naming
class color_hex_t(str):
    pass


# noinspection PyPep8Naming
class key_sequence_t(str):
    pass


# noinspection PyPep8Naming
class string_list_t(list):
    pass


# noinspection PyPep8Naming
class plain_dict_t(dict):
    pass


# noinspection PyPep8Naming
class json_obj_t(object):
    pass


# noinspection PyPep8Naming
class path_list_t(list):
    pass


# noinspection PyPep8Naming
class file_list_t(list):
    pass


# noinspection PyPep8Naming
class dir_list_t(list):
    pass


# noinspection PyPep8Naming
class font_t(str):
    pass


# noinspection PyPep8Naming
class int_quantity_t(tuple):
    pass


# noinspection PyPep8Naming
class float_quantity_t(tuple):
    pass


# noinspection PyPep8Naming
class string_dict_t(dict):
    pass


# noinspection PyPep8Naming
class paths_t(list):
    pass
