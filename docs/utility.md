## （一）概述

`PyGUIAdapter`提供了大量实用函数，开发者可以在窗口或`Action`的事件回调函数中调用这些函数，进一步扩展程序的功能。

这些函数可以在[`pyguiadapter.utils`]({{main_branch}}/pyguiadapter/utils/)包下找到，主要包含以下几个模块：

- [`filedialog`]({{main_branch}}/pyguiadapter/utils/filedialog.py)，主要提供文件选择对话框功能。
- [`messagebox`]({{main_branch}}/pyguiadapter/utils/messagebox.py)，主要提供消息对话框功能。
- [`inputdialog`]({{main_branch}}/pyguiadapter/utils/inputdialog.py)，主要提供输入对话框功能。
- [`editor`]({{main_branch}}/pyguiadapter/utils/editor.py) ，主要提供结构化对象编辑器功能。关于结构化对象及其编辑器，可以参考以下文档：
[结构化对象及其编辑器](schema_editor.md)

## （二）使用方法

### 1、导入模块

以`filedialog`模块为例，导入模块代码如下：

```python
from pyguiadapter.utils import filedialog
```

### 2、调用相应函数

比如，需要通过打开文件对话框选择文件路径，开发者可以调用`filedialog.get_open_file()`函数，代码如下：

```python
file_path = filedialog.get_open_file(window, title="打开文件", filters="文本文件 (*.txt);;所有文件 (*.*)")
if not file_path:
    # 用户取消选择文件
    ...
else:
    # 用户选择了文件，可以进行后续操作
    ...
```

其中，`window`参数是窗口对象，开发者在窗口或者`Action`的事件回调函数中可以访问到当前的窗口对象。这也是这些实用函数特别适合在事件回调函数中使用的原因：实用函数中有很多都需要一个窗口对象作为参数，而开发者基本上只有在各种事件回调函数中才有机会获取到当前窗口对象。

### 3、在窗口事件回调函数中调用实用函数

下面的示例展示了如何将窗口事件回调与实用函数结合使用，我们将实现一个简单的功能，在窗口关闭时弹出确认对话框，用户确认后再关闭窗口。

基本思路是：在窗口的`on_close`事件回调函数中调用`messagebox`模块的`show_question_message()`函数，并根据用户的选择决定是否关闭窗口。代码非常简单，如下所示：

```python
from pyguiadapter.adapter import GUIAdapter
from pyguiadapter.utils import messagebox
from pyguiadapter.window import SimpleWindowEventListener
from pyguiadapter.windows.fnexec import FnExecuteWindow


def foo(arg1: int, arg2: str, arg3: bool):
    pass


def on_close(window: FnExecuteWindow) -> bool:
    ret = messagebox.show_question_message(
        window, message="Are you sure you want to quit?"
    )
    if ret == messagebox.Yes:
        # when `on_close()` returns True, the window will be closed
        return True
    else:
        messagebox.show_info_message(window, message="Quit cancelled by user!")
        # when `on_close()` returns False, the window will not be closed
        # in other words, the close event will be ignored
        return False


if __name__ == "__main__":
    # create a window listener that listens for the `on_close` event
    event_listener = SimpleWindowEventListener(on_close=on_close)

    adapter = GUIAdapter()
    # add the `foo` function to the adapter with the `window_listener` argument set to the event_listener
    adapter.add(foo, window_listener=event_listener)
    adapter.run()
```

### 4、在`Action`事件回调函数中调用实用函数

开发者可以提供以下方式在`Action`事件回调函数中调用实用函数：

```python
def on_action_open(window: FnExecuteWindow, _: Action):
    ret = filedialog.get_open_file(
        window,
        title="Open File",
        start_dir="./",
        filters="JSON files(*.json);;Python files(*.py);;All files(*.*)",
    )
    if not ret:
        return
    messagebox.show_info_message(window, f"File will be opened: {ret}")
```

完整的示例代码如下：

```python
from pyguiadapter.action import Action, Separator
from pyguiadapter.adapter import GUIAdapter
from pyguiadapter.menu import Menu
from pyguiadapter.toolbar import ToolBar
from pyguiadapter.windows.fnexec import FnExecuteWindow
from pyguiadapter.utils import messagebox, filedialog


def on_action_about(window: FnExecuteWindow, _: Action):
    messagebox.show_info_message(
        parent=window,
        message="This is an example of toolbar and menu with custom actions.",
        title="About",
    )


def on_action_close(window: FnExecuteWindow, _: Action):
    ret = messagebox.show_question_message(
        window, "Are you sure you want to quit?", buttons=messagebox.Yes | messagebox.No
    )
    if ret == messagebox.Yes:
        window.close()


def on_action_open(window: FnExecuteWindow, _: Action):
    ret = filedialog.get_open_file(
        window,
        title="Open File",
        start_dir="./",
        filters="JSON files(*.json);;Python files(*.py);;All files(*.*)",
    )
    if not ret:
        return
    messagebox.show_info_message(window, f"File will be opened: {ret}")


def on_action_save(window: FnExecuteWindow, _: Action):
    ret = filedialog.get_save_file(
        window,
        title="Save File",
        start_dir="./",
        filters="JSON files(*.json);;All files(*.*)",
    )
    if not ret:
        return
    messagebox.show_info_message(window, f"File will be saved: {ret}")


def on_action_auto_theme(window: FnExecuteWindow, _: Action, checked: bool):
    if checked:
        messagebox.show_info_message(window, "Auto theme is selected.")


def on_action_light_theme(window: FnExecuteWindow, _: Action, checked: bool):
    if checked:
        messagebox.show_info_message(window, "Light theme is selected.")


def on_action_dark_theme(window: FnExecuteWindow, _: Action, checked: bool):
    if checked:
        messagebox.show_info_message(window, "Dark theme is selected.")


action_about = Action(
    text="About",
    icon="fa.info-circle",
    on_triggered=on_action_about,
)

action_open = Action(
    text="Open",
    icon="fa.folder-open",
    shortcut="Ctrl+O",
    on_triggered=on_action_open,
)

action_save = Action(
    text="Save",
    icon="fa.save",
    shortcut="Ctrl+S",
    on_triggered=on_action_save,
)

action_close = Action(
    text="Quit",
    icon="fa.close",
    shortcut="Ctrl+Q",
    on_triggered=on_action_close,
)

action_auto_them = Action(
    text="Auto",
    checkable=True,
    checked=True,
    on_toggled=on_action_auto_theme,
)

action_light_theme = Action(
    text="Light",
    checkable=True,
    on_toggled=on_action_light_theme,
)

action_dark_theme = Action(
    text="Dark",
    checkable=True,
    on_toggled=on_action_dark_theme,
)

submenu_theme = Menu(
    title="Theme",
    actions=[action_auto_them, action_light_theme, action_dark_theme],
    exclusive=True,
)
menu_file = Menu(
    title="File",
    actions=[
        action_open,
        action_save,
        Separator(),
        action_close,
        Separator(),
        submenu_theme,
    ],
)
menu_help = Menu(
    title="Help",
    actions=[action_about],
)


def menu_toolbar_example(arg1: int, arg2: str, arg3: bool):
    """
    This example shows how to add and config toolbar and menus to the window.
    @param arg1:
    @param arg2:
    @param arg3:
    @return:
    """
    pass


if __name__ == "__main__":
    adapter = GUIAdapter()
    adapter.add(menu_toolbar_example, window_toolbar=ToolBar(
        actions=[action_open, action_save, Separator(), action_close]
    ), window_menus=[menu_file, menu_help])
    adapter.run()
```

上述代码运行结果如下：

<div style="text-align:center">
    <img src="../assets/menu_toolbar_example.gif" />
</div>