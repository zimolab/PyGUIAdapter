from pyguiadapter.adapter import GUIAdapter
from pyguiadapter.windows import DocumentBrowserConfig
from pyguiadapter.windows.fnselect import FnSelectWindowConfig


def fn1():
    """
    This example shows how config the **function select window**
    """
    pass


def fn2():
    """
    This example shows how config the **function select window**
    """
    pass


def fn3():
    """
    This example shows how config the **function select window**
    """
    pass


def fn4():
    """
    This example shows how config the **function select window**
    """
    pass


if __name__ == "__main__":

    select_window_config = FnSelectWindowConfig(
        title="My Tool Kit",
        icon="fa5s.tools",
        default_fn_group_name="Group 1",
        default_fn_group_icon="fa.desktop",
        fn_group_icons={
            "Group 2": "fa.mobile",
            "Group 3": "fa.cloud",
        },
        size=(600, 400),
        icon_size=32,
        icon_mode=True,
        select_button_text="Go!",
        document_browser_width=400,
        document_browser_config=DocumentBrowserConfig(),
        always_on_top=True,
    )

    adapter = GUIAdapter()
    adapter.add(fn1)
    adapter.add(fn2)
    adapter.add(fn3, group="Group 2")
    adapter.add(fn4, group="Group 3")
    adapter.run(select_window_config=select_window_config)
