from typing import Literal

from pyguiadapter.adapter import GUIAdapter, utoast
from pyguiadapter.exceptions import ParameterError
from pyguiadapter.extend_types import text_t, color_hex_t, int_slider_t
from pyguiadapter.toast import ToastConfig, AlignLeft, AlignRight, AlignCenter


def utoast_example(
    message: text_t,
    duration: int = 3000,
    opacity: float = 0.9,
    fade_out: int = 500,
    text_align: Literal["left", "right", "center"] = "center",
    text_padding: int = 50,
    background_color: color_hex_t = "#323232",
    text_color: color_hex_t = "#FFFFFF",
    font_size: int = 26,
    font_family: str = "Consolas",
    position_x: int_slider_t = 50,
    position_y: int_slider_t = 50,
):
    """
    Show a toast message on the screen.

    Args:
        message: The message to be displayed.
        duration: The duration of the toast message in milliseconds.
        opacity: The opacity of the toast message.
        fade_out: The duration of the fade out animation in milliseconds.
        text_align: The alignment of the text inside the toast message.
        text_padding: The padding of the text inside the toast message.
        background_color: The background color of the toast message.
        text_color: The text color of the toast message.
        font_size: The font size of the text inside the toast message.
        font_family: The font family of the text inside the toast message.
        position_x: The x position (by percentage) of the toast message on the screen.
        position_y: The y position (by percentage) of the toast message on the screen.

    @params
    [opacity]
    min_value = 0.0
    max_value = 1.0
    step = 0.01

    [position_x]
    min_value = 0
    max_value = 100
    prefix = "x: "
    suffix = "%"

    [position_y]
    min_value = 0
    max_value = 100
    prefix = "y: "
    suffix = "%"

    [background_color]
    alpha_channel = false

    [text_color]
    alpha_channel = false

    @end

    """
    if not message or message.strip() == "":
        raise ParameterError(
            parameter_name="message", message="Message cannot be empty."
        )

    if text_align == "left":
        align = AlignLeft
    elif text_align == "right":
        align = AlignRight
    else:
        align = AlignCenter

    position_x = float(position_x) / 100.0
    position_y = float(position_y) / 100.0

    toast_config = ToastConfig(
        opacity=opacity,
        background_color=background_color,
        text_color=text_color,
        text_padding=text_padding,
        text_alignment=align,
        font_size=font_size,
        font_family=font_family,
        position=(position_x, position_y),
        fade_out=fade_out,
    )
    utoast.show_toast(message, duration, toast_config)


if __name__ == "__main__":
    adapter = GUIAdapter()
    adapter.add(utoast_example)
    adapter.run()
