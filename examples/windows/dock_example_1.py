from pyguiadapter.adapter import GUIAdapter
from pyguiadapter.windows.fnexec import RightDockWidgetArea, FnExecuteWindowConfig


def dock_area_example_1():
    """
    This example shows how to change the dock area and initial size of the output and document docks.
    @return:
    """
    pass


if __name__ == "__main__":
    adapter = GUIAdapter()
    adapter.add(
        dock_area_example_1,
        window_config=FnExecuteWindowConfig(
            document_dock_initial_size=(614, 538),
            output_dock_initial_area=RightDockWidgetArea,
            output_dock_initial_size=(None, 230),
        ),
    )
    adapter.run()
