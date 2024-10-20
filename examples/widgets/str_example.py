from pyguiadapter.adapter import GUIAdapter
from pyguiadapter.adapter.uoutput import uprint
from pyguiadapter.widgets import LineEditConfig, LineEdit


def str_example(
    str_arg1: str = "arg1",
    str_arg2: str = "arg2",
    str_arg3: str = "arg3",
    str_arg4: str = "arg4",
    str_arg5: str = "arg5",
):
    """
    example for type **str** and **LineEdit** widget

    @param str_arg1: this parameter will be configured in docstring
    @param str_arg2: this parameter will be configured in docstring
    @param str_arg3: this parameter will be configured in docstring
    @param str_arg4: this parameter will be configured with adapter.run() via a LineEditConfig object
    @param str_arg5: this parameter will be configured with adapter.run() via a dict
    @return:

    @params
    [str_arg1]
    # override the default value of str_arg1 defined in the function signature
    default_value = "123456"
    clear_button_enabled = true
    max_length = 5
    frame = false

    [str_arg2]
    input_mask = "000.000.000.000;_"

    [str_arg3]
    default_value = ""
    placeholder = "this is a placeholder text"


    @end

    """
    uprint("str_example")
    uprint("str_arg1:", str_arg1)
    uprint("str_arg2:", str_arg2)
    uprint("str_arg3:", str_arg3)
    uprint("str_arg4:", str_arg4)
    uprint("str_arg5:", str_arg5)
    return str_arg1 + str_arg2 + str_arg3 + str_arg4 + str_arg5


if __name__ == "__main__":

    str_arg4_conf = LineEditConfig(
        # override the default value of str_arg4 defined in the function signature
        default_value="this is a readonly text",
        readonly=True,
        echo_mode=LineEdit.EchoMode.Password,
    )

    str_arg5_conf = {
        "validator": r"^[a-zA-Z0-9]+$",
        "alignment": LineEdit.Alignment.AlignRight,
    }

    adapter = GUIAdapter()
    adapter.add(
        str_example,
        widget_configs={
            "str_arg4": str_arg4_conf,
            "str_arg5": str_arg5_conf,
        },
    )
    adapter.run()
