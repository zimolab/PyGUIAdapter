## （一）窗口概述

`PyGUIAdapter`中主要有两种类型的窗口：`函数选择窗口（FnSelectWindow）`和`函数执行窗口（FnExecuteWindow）`，它们都继承自窗口父类[`BaseWindow`]({{main_branch}}/pyguiadapter/window.py)。`BaseWindow`定义了子类窗口的共同行为，比如：

- 开发者可以使用`窗口配置类`配置窗口的某些属性
- 开发者可以向窗口中添加工具栏和菜单栏
- 开发者可以监听窗口的某些事件
- 开发者可以在窗口事件回调中获取/改变添加到工具栏（菜单栏）中的`动作（Action）`的状态
- ......

### 1、窗口的基本接口

同时， `BaseWindow`中定义并实现了一组基本接口，这些接口可以对窗口进行操作或者是实现了其他有用的功能，开发者可以在`动作（Action）`或窗口事件的回调函数中调用这些接口。可以参考这个文档[`pyguiadapter.window.BaseWindow`](apis/pyguiadapter.window.md#pyguiadapter.window.BaseWindow)以获取这些接口的详细信息。

### 2、窗口的共同属性

窗口的属性，如标题、图标、大小、位置、字体、样式等，均由窗口的配置类定义，[`BaseWindowConfig`]({{main_branch}}/pyguiadapter/window.py)是所有窗口配置类的父类，定义了一组所有窗口均适用的共同属性，可以参考这个文档[`pyguiadapter.window.BaseWindowConfig`](apis/pyguiadapter.window.md#pyguiadapter.window.BaseWindowConfig)以获取这些属性的详细信息。

 `BaseWindow`的子类窗口通常继承`BaseWindowConfig`实现专用的窗口配置类，并覆盖`BaseWindowConfig`中某些属性的默认值或添加专门适用于子类窗口的新属性。

### 3、窗口事件监听

窗口的创建、显示、关闭、销毁、隐藏均被视为一种事件，开发者可以监听这些事件，并在这些事件发生时执行特定的代码。对窗口事件的监听，需要通过[`BaseWindowEventListener`]({{main_branch}}/pyguiadapter/window.py)对象来完成，开发者可以子类化该类，或者使用一个它的一个现成的子类[`SimpleWindowEventListener`]({{main_branch}}/pyguiadapter/window.py)。

可以参考以下文档获取窗口事件的详细信息：

- [`pyguiadapter.window.BaseWindowEventListener`](apis/pyguiadapter.window.md#pyguiadapter.window.BaseWindowEventListener)
- [`pyguiadapter.window.SimpleWindowEventListener`](apis/pyguiadapter.window.md#pyguiadapter.window.SimpleWindowEventListener)

## （二）函数选择窗口（FnSelectWindow）

### 1、概述

在向`GUIAdapter`实例中添加了多个函数后，`PyGUIAdapter`将创建一个`函数选择窗口`，该窗口会显示所有已添加的函数。在仅添加了一个函数时，`函数选择窗口`将不会显示，而是直接显示该函数的执行窗口，当然，开发者也可以通过如下方式，强制显示`函数选择窗口`：

```python
adapter.run(show_select_window=True)
```

`函数选择窗口`主要分成三个区域：

- ①`函数列表区域`
- ②`函数文档区域`
- ③`函数选择按钮`

<div style="text-align:center">
    <img src="/assets/fn_select_window_areas.png" />
</div>

### 2、配置窗口属性

`函数选择窗口（FnSelectWindow）`的可配置属性由`FnSelectWindowConfig`类定义，开发者可以通过以下方法配置窗口属性：



<div style="text-align:center">
    <img src="/assets/fn_select_window_config_3.png" />
</div>
完整代码如下：

```python
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
```

<div style="text-align: center">
    <img src="/assets/fn_select_window_config_1.png" />
</div>

<div style="text-align: center">
    <img src="/assets/fn_select_window_config_2.png" />
</div>




关于`函数选择窗口（FnSelectWindow）`的可配置属性，可参考以下文档：

- [pyguiadapter.windows.fnselect.FnSelectWindowConfig](apis/pyguiadapter.windows.fnselect.md#pyguiadapter.windows.fnselect.FnSelectWindowConfig)

### 3、监听窗口事件

开发者可以对`函数选择窗口（FnSelectWindow）`的事件进行监听。方法如下：

<div style="text-align: center">
    <img src="/assets/fn_select_window_config_8.png" />
</div>

完整代码如下：

```python
from pyguiadapter.adapter import GUIAdapter
from pyguiadapter.utils import messagebox
from pyguiadapter.window import SimpleWindowEventListener
from pyguiadapter.windows.fnselect import FnSelectWindow


def on_window_create(window: FnSelectWindow):
    print("on_create")


def on_window_show(window: FnSelectWindow):
    print("on_show")


def on_window_hide(window: FnSelectWindow):
    print("on_hide")


def on_window_close(window: FnSelectWindow) -> bool:
    print("on_close")
    ret = messagebox.show_question_message(
        window,
        title="Confirm Quit",
        message="Are you sure to quit?",
        buttons=messagebox.Yes | messagebox.No,
    )
    if ret == messagebox.Yes:
        return True
    return False


def on_window_destroy(window: FnSelectWindow):
    print("on_destroy")


def event_example_3():
    pass


if __name__ == "__main__":
    event_listener = SimpleWindowEventListener(
        on_create=on_window_create,
        on_show=on_window_show,
        on_hide=on_window_hide,
        on_close=on_window_close,
        on_destroy=on_window_destroy,
    )
    adapter = GUIAdapter()
    adapter.add(event_example_3)
    adapter.run(show_select_window=True, select_window_listener=event_listener)

```

代码运行效果如下：

<div style="text-align: center">
    <img src="/assets/fn_select_window_config_9.png" />
</div>

控制台输出如下：

<div style="text-align: center">
    <img src="/assets/fn_select_window_config_10.png" />
</div>

### 4、添加工具栏

开发者可以向`函数选择窗口（FnSelectWindow）`中添加工具栏，方法如下：

<div style="text-align: center">
    <img src="/assets/fn_select_window_toolbar.png" />
</div>

完整代码如下：

```python
from pyguiadapter.action import Action
from pyguiadapter.adapter import GUIAdapter
from pyguiadapter.toolbar import ToolBar, ToolButtonTextUnderIcon
from pyguiadapter.utils import messagebox
from pyguiadapter.windows.fnselect import FnSelectWindow


def on_action_test(window: FnSelectWindow, action: Action):
    messagebox.show_info_message(
        window, message=f"Action Triggered!(Action: {action.text})"
    )


def on_action_close(window: FnSelectWindow, _: Action):
    ret = messagebox.show_question_message(
        window,
        message="Are you sure to close the application?",
        buttons=messagebox.Yes | messagebox.No,
    )
    if ret == messagebox.Yes:
        window.close()


action_test = Action(
    text="Test", icon="fa.folder-open", on_triggered=on_action_test, shortcut="Ctrl+O"
)
action_close = Action(
    text="Close", icon="fa.close", on_triggered=on_action_close, shortcut="Ctrl+Q"
)

toolbar = ToolBar(
    actions=[action_test, action_close],
    floatable=True,
    button_style=ToolButtonTextUnderIcon,
)


def foo():
    pass


if __name__ == "__main__":
    adapter = GUIAdapter()
    adapter.add(foo)
    adapter.run(show_select_window=True, select_window_toolbar=toolbar)

```

效果如下：

<div style="text-align: center">
    <img src="/assets/fn_select_window_toolbar.gif" />
</div>

### 5、添加窗口菜单

开发者可以向`函数选择窗口（FnSelectWindow）`中添加菜单栏，方法如下：

<div style="text-align: center">
    <img src="/assets/fn_select_window_config_6.png" />
</div>

完整示例代码如下：

```python
from pyguiadapter.action import Action, Separator
from pyguiadapter.adapter import GUIAdapter
from pyguiadapter.menu import Menu
from pyguiadapter.utils import messagebox
from pyguiadapter.windows.fnselect import FnSelectWindow


def on_action_test(window: FnSelectWindow, action: Action):
    messagebox.show_info_message(
        window, message=f"Action Triggered!(Action: {action.text})"
    )


def on_action_close(window: FnSelectWindow, _: Action):
    ret = messagebox.show_question_message(
        window,
        message="Are you sure to close the application?",
        buttons=messagebox.Yes | messagebox.No,
    )
    if ret == messagebox.Yes:
        window.close()


action_test = Action(
    text="Test", icon="fa.folder-open", on_triggered=on_action_test, shortcut="Ctrl+O"
)
action_close = Action(
    text="Close", icon="fa.close", on_triggered=on_action_close, shortcut="Ctrl+Q"
)


menu_file = Menu(
    title="File",
    actions=[action_test, Separator(), action_close],
)


def foo():
    pass


if __name__ == "__main__":
    adapter = GUIAdapter()
    adapter.add(foo)
    adapter.run(show_select_window=True, select_window_menus=[menu_file])

```

效果如下：

<div style="text-align: center">
    <img src="/assets/fn_select_window_menu.gif" />
</div>

### 6、主要接口

参考：[pyguiadapter.windows.fnselect.FnSelectWindow](apis/pyguiadapter.windows.fnselect.md#pyguiadapter.windows.fnselect.FnSelectWindow)。

## （三）函数执行窗口（FnExecuteWindow）




