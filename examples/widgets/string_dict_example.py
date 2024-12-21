from pyguiadapter.adapter import GUIAdapter
from pyguiadapter.adapter.uoutput import uprint
from pyguiadapter.extend_types import string_dict_t


def string_dict_example(arg1: string_dict_t, arg2: string_dict_t, arg3: string_dict_t):
    """
    This is an example for **StringDictEdit** for **string_dict_t** types.

    Args:
        arg1: description of arg1.
        arg2: description of arg2.
        arg3: description of arg3.

    Returns:
        None.

    @params
    [arg1]
    default_value = {"key1"="value1", "key2"="value2", "key3"="value3", "key4"="value4", "key5"="value5"}

    @end

    """
    uprint("arg1:", arg1)
    uprint("arg2:", arg2)
    uprint("arg3:", arg3)


if __name__ == "__main__":
    adapter = GUIAdapter()
    adapter.add(string_dict_example)
    adapter.run()
