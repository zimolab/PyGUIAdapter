from pyguiadapter.adapter import GUIAdapter
from pyguiadapter.exceptions import ParameterError
from pyguiadapter.windows import FnExecuteWindowConfig, MessageTexts


def window_messages_customization(a: int, b: int):
    """
    This function will return `a / b`

    when a < 0 or b > 100, it will raise a **ParameterError**

    """
    if a < 0:
        raise ParameterError(parameter_name="a", message="a must be >= 0")

    if b > 100:
        raise ParameterError(parameter_name="b", message="b must be <= 100")

    return a / b


if __name__ == "__main__":

    message_texts = MessageTexts(
        function_result="You got: {}",
    )

    adapter = GUIAdapter()
    adapter.add(
        window_messages_customization,
        window_config=FnExecuteWindowConfig(
            title="Window Messages Customization Demo",
            default_parameter_group_name="Parameters",
            message_texts=message_texts,
            show_function_error=True,
            show_function_result=True,
        ),
    )
    adapter.run()
