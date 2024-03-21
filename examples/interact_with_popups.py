from pyguiadapter.adapter import GUIAdapter


def interact_with_popups(popup_type: str = "get_int"):
    """
    This demo shows how interact with user by using popups

    :param popup_type: <b color="red">Select the popup type </b>
    :return:

    @begin
    [popup_type]
    type="RadioButtonGroup"
    items=["get_int", "get_float", "get_text"]
    column_count=3
    @end
    """
    return 1 / 0


gui_adapter = GUIAdapter()
gui_adapter.execution_window_config.show_function_result_dialog = False
gui_adapter.add(interact_with_popups)
gui_adapter.run()
