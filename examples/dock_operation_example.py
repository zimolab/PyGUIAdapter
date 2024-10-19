from pyguiadapter.action import Action, Separator
from pyguiadapter.adapter import GUIAdapter
from pyguiadapter.menu import Menu
from pyguiadapter.windows.fnexec import (
    FnExecuteWindow,
    BottomDockWidgetArea,
)


def dock_operation_example() -> None:
    pass


def on_toggle_document_dock(win: FnExecuteWindow, action: Action):
    win.set_document_dock_property(visible=not win.is_document_dock_visible())


def on_toggle_output_dock(win: FnExecuteWindow, action: Action):
    win.set_output_dock_property(visible=not win.is_output_dock_visible())


def on_tabify_docks(win: FnExecuteWindow, action: Action):
    win.tabify_docks()


def on_move_output_area(win: FnExecuteWindow, action: Action):
    if win.is_output_dock_floating():
        win.set_output_dock_property(floating=False)
    win.set_output_dock_property(area=BottomDockWidgetArea)


def on_float_output_dock(win: FnExecuteWindow, action: Action):
    win.set_output_dock_property(floating=True)


def main():
    action_document_dock = Action(
        text="Toggle Document Dock",
        on_triggered=on_toggle_document_dock,
    )
    action_output_dock = Action(
        text="Toggle Output Dock",
        on_triggered=on_toggle_output_dock,
    )
    action_tabify_docks = Action(
        text="Tabify Docks",
        on_triggered=on_tabify_docks,
    )
    action_move_output_area = Action(
        text="Move Output Area",
        on_triggered=on_move_output_area,
    )
    action_float_output_dock = Action(
        text="Float Output Dock",
        on_triggered=on_float_output_dock,
    )
    menu_views = Menu(
        title="Views",
        actions=[
            action_document_dock,
            action_output_dock,
            Separator(),
            action_tabify_docks,
            action_move_output_area,
            action_float_output_dock,
        ],
    )
    ##########
    adapter = GUIAdapter()
    adapter.add(dock_operation_example, window_menus=[menu_views])
    adapter.run()


if __name__ == "__main__":
    main()
