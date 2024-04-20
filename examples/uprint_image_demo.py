import os.path
from function2widgets import (
    FilePathEdit,
    FilePathEditArgs,
    LineEdit,
    LineEditArgs,
    CheckBox,
    CheckBoxArgs,
)

from pyguiadapter.interact.uprint import uprint_image


def create_file(image_path: str, alt_text: str, blank_lines_around: bool):
    if not image_path:
        raise ValueError("image_path is empty")
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"image file not found: {image_path}")
    uprint_image(image_path, alt_text, blank_lines_around)


if __name__ == "__main__":
    from pyguiadapter import GUIAdapter

    widget_configs = {
        "image_path": {
            "widget_class": FilePathEdit.__name__,
            "widget_args": FilePathEditArgs(
                parameter_name="AS-IS",
                label="Image Path",
                default="",
                button_text="select img file",
                filters="Image files (*.png *.jpg *.jpeg *.bmp *.gif)",
                start_path="./",
                dialog_title="Select img file",
            ),
        },
        "alt_text": {
            "widget_class": LineEdit.__name__,
            "widget_args": LineEditArgs(
                parameter_name="AS-IS",
                label="Alt Text",
                description="this text will show when the image not loaded",
                default="",
                placeholder="enter alt text here",
            ),
        },
        "blank_lines_around": {
            "widget_class": CheckBox.__name__,
            "widget_args": CheckBoxArgs(
                parameter_name="AS-IS",
                label="Blank Lines",
                description="whether to add blanks lines around the image",
                default=False,
                text="Add blank lines around the image",
            ),
        },
    }

    gui_adapter = GUIAdapter()
    gui_adapter.add(create_file, widget_configs=widget_configs)
    gui_adapter.run()
