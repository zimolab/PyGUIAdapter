from pyguiadapter.adapter import GUIAdapter
from pyguiadapter.windows import WidgetTexts, FnExecuteWindowConfig


def window_texts_customization():
    pass


if __name__ == "__main__":

    win_widget_text = WidgetTexts(
        document_dock_title="Function  Document",
        output_dock_title="Function Output",
        execute_button_text="Start!",
        clear_button_text="Clear output",
        clear_checkbox_text="clear function output before executing",
    )

    adapter = GUIAdapter()
    adapter.add(
        window_texts_customization,
        window_config=FnExecuteWindowConfig(
            title="Window Texts Customization Demo",
            default_parameter_group_name="Parameters",
            widget_texts=win_widget_text,
        ),
    )
    adapter.run()
