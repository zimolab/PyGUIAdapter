## 函数执行窗口（FnExecuteWindow）

### 一、简介

`函数执行窗口（FnExecuteWindow）`是用户与程序进行交互的主要界面。一个典型的`函数执行窗口（FnExecuteWindow）`由以下几个部分组成：

<img src="../images/solver.png" />

包括一个固定区域（`Parameters Area`）和两个停靠窗口（`Document Dock`和`Output Dock`）。

1. **参数控件区（Parameters Area）**：主要用于放置函数参数控件。

2. **函数文档停靠窗口（Document Dock）**：主要用于显示函数的文档信息。默认情况下，其内容来源于函数的`文档字符串（docstring）`。

3. **程序输出停靠窗口（Output Dock）**：主要用于显示程序的输出信息。默认情况下，函数的返回值、函数调用过程中发生的异常信息均会显示在此区域。

### 二、配置窗口属性

#### （一）配置类`FnExecuteWindowConfig`

`函数执行窗口（FnExecuteWindow）`的窗口属性由配置类`FnExecuteWindowConfig`定义，该类定义了`函数执行窗口（FnExecuteWindow）`有以下可配置属性。

> `FnExecuteWindow`与`FnExecuteWindowConfig`均在`pyguiadapter.windows.fnexec`包下，可通过以下方式导入：
>
> ```python
> from pyguiadapter.windows.fnexec import FnExecuteWindowConfig
> from pyguiadapter.windows.fnexec import FnExecuteWindow
> ```



|            配置项名称            |                             类型                             |               默认值                |                             说明                             |
| :------------------------------: | :----------------------------------------------------------: | :---------------------------------: | :----------------------------------------------------------: |
|             `title`              |                    `Union[str, NoneType]`                    |               `None`                | 窗口标题。默认为`None`，此时将使用函数的显示名称（`display_name`）作为窗口标题（如果开发者未指定`display_name`，则其等同于函数名，关于如何指定`display_name`，可以参考这篇文档：[函的数名称、图标、文档及分组](adapter/multiple_functions.md??id=二、修改函数图标和显示名称)。） |
|              `icon`              | `Union[str, Tuple[str, Union[list, dict]], QIcon, QPixmap, NoneType]` |               `None`                | 窗口图标。如果开发者未指定窗口图标，则将使用添加函数时指定的`icon`。（关于如何在添加函数指定其`icon`，可以参考这篇文档：[函的数名称、图标、文档及分组](adapter/multiple_functions.md??id=二、修改函数图标和显示名称)。） |
|              `size`              |               `Union[Tuple[int, int], QSize]`                |            `(1024, 768)`            |                         窗口的尺寸。                         |
|            `position`            |              `Union[Tuple[int, int], NoneType]`              |               `None`                | 窗口的位置，默认为`None`，即使用系统默认值，一般是居中显示。 |
|         `always_on_top`          |                            `bool`                            |               `False`               |                      窗口是否总是置顶。                      |
|          `font_family`           |            `Union[str, Sequence[str], NoneType]`             |               `None`                |                       窗口的字体家族。                       |
|           `font_size`            |                    `Union[int, NoneType]`                    |               `None`                |                       窗口的字体大小。                       |
|           `stylesheet`           |                    `Union[str, NoneType]`                    |               `None`                |                        窗口的样式表。                        |
|      `execute_button_text`       |                            `str`                             |             `"Execute"`             |              执行按钮的文字。默认为"Execute"。               |
|       `cancel_button_text`       |                            `str`                             |             `"Cancel"`              | 取消按钮的文字。默认为"Cancel"。注意，只有当函数被标记为`cancelable`才会出现取消按钮。如何将函数标记为`cancelable`，可以参考这篇文档：[取消正在执行的函数：协商式线程退出机制](adapter/cancellable_function.md) |
|      `clear_button_visible`      |                            `bool`                            |               `True`                |    是否显示清除输出按钮。开发者可以通过此属性隐藏该按钮。    |
|       `clear_button_text`        |                            `str`                             |              `"Clear"`              |                     清除输出按钮的文字。                     |
|     `clear_checkbox_visible`     |                            `bool`                            |               `True`                |                    是否显示清除输出选框。                    |
|     `clear_checkbox_checked`     |                            `bool`                            |               `True`                |          是否将清除输出选框初始状态设置为勾选状态。          |
|       `statusbar_visible`        |                            `bool`                            |               `True`                |                   是否显示窗口底部状态栏。                   |
|      `initial_docks_state`       |                `Literal["auto", "tabified"]`                 |              `"auto"`               | 停靠窗口的初始状态。当设置为`"tabified"`时，所有停靠窗口会显示出标签页的形式。默认为`"auto"`，即分开显示。 |
|      `output_dock_visible`       |                            `bool`                            |               `True`                |                   是否显示`Output Dock`。                    |
|       `output_dock_title`        |                            `str`                             |             `"Output"`              |                    `Output Dock`的标题。                     |
|      `output_dock_floating`      |                            `bool`                            |               `False`               |            是否使`Output Dock`漂浮在主窗体之上。             |
|    `output_dock_initial_area`    |                       `DockWidgetArea`                       |       `BottomDockWidgetArea`        | `Output Dock`的初始停靠位置，默认为`BottomDockWidgetArea`，即停靠在窗体的下部。 |
|    `output_dock_initial_size`    |            `Tuple[Optional[int], Optional[int]]`             |            `(None, 230)`            | `Output Dock`的初始大小，默认为`(None, 230)`，即宽度与主窗口一致，高度为`230`（默认窗口高度的30%）。 |
|     `document_dock_visible`      |                            `bool`                            |               `True`                |                  是否显示`Document Dock`。                   |
|      `document_dock_title`       |                            `str`                             |            `"Document"`             |                   `Document Dock`的标题。                    |
|     `document_dock_floating`     |                            `bool`                            |               `True`                |           是否使`Document Dock`漂浮在主窗体之上。            |
|   `document_dock_initial_area`   |                       `DockWidgetArea`                       |        `RightDockWidgetArea`        | `Document Dock`的初始停靠位置，默认为`RightDockWidgetArea`，即停靠在窗体的下部。 |
|   `document_dock_initial_size`   |            `Tuple[Optional[int], Optional[int]]`             |            `(614, None)`            | `Document Dock`的初始大小，默认为`(614, None)`，即宽度为614（默认窗口宽度的60%），高度与主窗口一致。 |
|     `output_browser_config`      |               `Optional[OutputBrowserConfig]`                |               `None`                |                    程序输出浏览器的配置。                    |
|    `document_browser_config`     |              `Optional[DocumentBrowserConfig]`               |               `None`                |                    函数文档浏览器的配置。                    |
|  `default_parameter_group_name`  |                            `str`                             |         `"Main Parameters"`         |                     默认参数分组的名称。                     |
|  `default_parameter_group_icon`  |                          `IconType`                          |               `None`                |                     默认参数分组的图标。                     |
|     `parameter_group_icons`      |                    `Dict[str, IconType]`                     |                `{}`                 |                   各个参数分组对应的图标。                   |
|     `print_function_result`      |                            `bool`                            |               `True`                |               是否在输出区域打印函数调用结果。               |
|      `show_function_result`      |                            `bool`                            |               `False`               |                  是否弹窗显示函数调用结果。                  |
|      `print_function_error`      |                            `bool`                            |               `True`                |         是否在输出区域打印函数调用过程中的异常信息。         |
|      `show_function_error`       |                            `bool`                            |               `True`                |            是否弹窗显示函数调用过程中的异常信息。            |
|    `function_error_traceback`    |                            `bool`                            |               `True`                |                   是否显示异常的回溯信息。                   |
|       `error_dialog_title`       |                            `str`                             |              `"Error"`              |                   错误（异常）弹窗的标题。                   |
|      `result_dialog_title`       |                            `str`                             |             `"Result"`              |                     函数结果弹窗的标题。                     |
|    `parameter_error_message`     |                            `str`                             |             `"{}: {}"`              | `ParameterError`类异常的消息模板。模板第一个位置将被替换为发生`ParameterError`的参数的名称，第二个位置将被替换为该异常的描述消息。 |
|    `function_result_message`     |                            `str`                             |      `"function result: {}\n"`      |                     函数结果的消息模板。                     |
|     `function_error_message`     |                            `str`                             |            `"{}: {}\n"`             | 函数异常的消息模板。第一个位置将被替换为异常类的名称，第二个位置将被替换为异常的消息。 |
|   `function_executing_message`   |                            `str`                             |  `"A function is executing now!"`   | 消息字符串。当用户意图执行一项操作，而该操作又不允许在函数正在执行时进行的情况下，会发出此提示。比如，函数正在进行，用户要关闭窗口。 |
| `uncancelable_function_message`  |                            `str`                             | `"The function is not cancelable!"` | 消息字符串。当函数为”不可取消“的，而用户又发出取消函数信号时，将提示此消息。 |
| `function_not_executing_message` |                            `str`                             |  `"No function is executing now!"`  | 消息字符串。当一项操作又必须在运行时进行，而函数恰好又不在运行状态时，将提示此消息。比如，取消操作必须在函数正在运行时才有效，当函数不在运行时，发出取消信号，将提示此消息。 |

**关于`DocumentBrowserConfig`：** 该类用于配置文档浏览器属性，在[`pyguiadapter.windows.document_browser.DocumentBrowserConfig`]()中定义，可以通过如下方式引入：

```python
from pyguiadapter.windows import DocumentBrowserConfig
```

文档浏览器主要包含以下属性：

|      配置项名称       |            类型             |                默认值                 |                       说明                       |
| :-------------------: | :-------------------------: | :-----------------------------------: | :----------------------------------------------: |
|     `text_color`      |            `str`            |               `#000000`               |              文本颜色。默认为黑色。              |
|     `font_family`     | `Union[Sequence[str], str]` | `('Consolas', 'Arial', 'sans-serif')` |                  文本字体系列。                  |
|      `font_size`      |            `int`            |                 `12`                  |                  文本字体大小。                  |
|  `background_color`   |            `str`            |               `#FFFFFF`               |              背景颜色。默认为白色。              |
|   `line_wrap_mode`    |       `LineWrapMode`        |      `LineWrapMode.WidgetWidth`       |        行包裹模式。默认根据控件宽度换行。        |
|   `line_wrap_width`   |            `int`            |                 `88`                  |                   行包裹宽度。                   |
|   `word_wrap_mode`    |         `WrapMode`          |          `WrapMode.WordWrap`          |                   词包裹模式。                   |
| `open_external_links` |           `bool`            |                `True`                 | 是否可以允许调用系统浏览器打开文档中的外部链接。 |
|     `stylesheet`      |            `str`            |                 `""`                  |                     样式表。                     |

下图时默认状态下文档浏览器的典型外观：

<img src="../images/default_document_browser.png" />

**关于`OutputBrowserConfig`**：该类用于配置输出浏览器的属性，可以通过以下方式导入：

> ```python
> from pyguiadapter.windows.fnexec import OutputBrowserConfig
> ```

输出浏览器主要具有以下属性：

|      配置项名称       |            类型             |                默认值                 |                       说明                       |
| :-------------------: | :-------------------------: | :-----------------------------------: | :----------------------------------------------: |
|     `text_color`      |            `str`            |               `#000000`               |              文本颜色。默认为黑色。              |
|     `font_family`     | `Union[Sequence[str], str]` | `('Consolas', 'Arial', 'sans-serif')` |                  文本字体系列。                  |
|      `font_size`      |            `int`            |                 `12`                  |                  文本字体大小。                  |
|  `background_color`   |            `str`            |               `#FFFFFF`               |              背景颜色。默认为白色。              |
|   `line_wrap_mode`    |       `LineWrapMode`        |      `LineWrapMode.WidgetWidth`       |        行包裹模式。默认根据控件宽度换行。        |
|   `line_wrap_width`   |            `int`            |                 `88`                  |                   行包裹宽度。                   |
|   `word_wrap_mode`    |         `WrapMode`          |          `WrapMode.WordWrap`          |                   词包裹模式。                   |
| `open_external_links` |           `bool`            |                `True`                 | 是否可以允许调用系统浏览器打开文档中的外部链接。 |
|     `stylesheet`      |            `str`            |                 `""`                  |                     样式表。                     |

下图时默认情况下输出浏览器的典型外观：

<img src="../images/default_output_browser.png" />

**为什么设置了`DocumentBrowserConfig`和`OutputBrowserConfig`，但有时就是不生效？**

这种情况常见于开发者设置了样式表（qss）或使用了第三方美化库时。第三方美化库对窗口和控件样式的改变基本上都是通过样式表实现的，样式表的优先级要高于`DocumentBrowserConfig`和`OutputBrowserConfig`，因此可能会发生`DocumentBrowserConfig`或`OutputBrowserConfig`设置的样式（如文字颜色、背景色等）被外部样式表覆盖掉，因此看起来像没生效的情况。这可以说是有意为之的一种设计，目的是让文档浏览器和输出浏览器的外观与界面整体风格保持一致。

比如下面这个例子，在设置了`dark`主题后，文档浏览器和输出浏览器的文字颜色、背景颜色等被第三方库调整到合适的状态，如果此时文档浏览器还是默认白底黑字的配色，则会显得有些格格不入。

> [examples/adapter/qdarktheme_example.py]()

```python
"""
This example requires PyQtDarkTheme. Please install it before you run this example.
"""

from datetime import datetime

from pyguiadapter.adapter import GUIAdapter
from pyguiadapter.extend_types import text_t


def app_style_example(
    arg1: str, arg2: int, arg3: float, arg4: bool, arg5: text_t, arg6: datetime
):
    """
    This example requires [PyQtDarkTheme](https://github.com/5yutan5/PyQtDarkTheme).
    Please install it before you run the example.

    <br />

    e.g. using `pip`:

    > `pip install pyqtdarktheme`

    @param arg1: arg1 description
    @param arg2: arg2 description
    @param arg3: arg3 description
    @param arg4: arg4 description
    @param arg5: arg5 description
    @param arg6: arg6 description
    @return:
    """
    pass


if __name__ == "__main__":
    import qdarktheme

    def on_app_start(app):
        # this will be called after the instantiation of QApplication.
        print("app started")
        qdarktheme.setup_theme("dark")

    adapter = GUIAdapter(on_app_start=on_app_start)
    adapter.add(app_style_example)
    adapter.run()

```

<img src="../images/style_override.png" />

如果开发者确实需要自行设置文档浏览器或输出浏览器的样式，而不希望它被第三方库覆盖，可以通过`DocumentBrowserConfig`或`OutputBrowserConfig`的`stylesheet`属性明确指明所需的样式表，通过`stylesheet`设置的样式一般不会被第三方库覆盖。比如下面的示例，强行将输出浏览器设置为以下样式（其他控件的样式由第三方库决定）：

- 背景色：`#380C2A`
- 文字颜色：`#FFFFFF`
- 字体系列：`Consolas`
- 字体大小：`12pt`

> [examples/windows/style_override_example.py]()

```python
"""
This example requires PyQtDarkTheme. Please install it before you run this example.
"""

from datetime import datetime

from pyguiadapter.adapter import GUIAdapter
from pyguiadapter.extend_types import text_t
from pyguiadapter.windows.fnexec import FnExecuteWindowConfig, OutputBrowserConfig


def app_style_example(
    arg1: str, arg2: int, arg3: float, arg4: bool, arg5: text_t, arg6: datetime
):
    """
    This example requires [PyQtDarkTheme](https://github.com/5yutan5/PyQtDarkTheme).
    Please install it before you run the example.
    <br />

    e.g. using `pip`:

    > `pip install pyqtdarktheme`

    <br />

    The style of output browser will be overridden with **OutputBrowserConfig.stylesheet**

    @param arg1: arg1 description
    @param arg2: arg2 description
    @param arg3: arg3 description
    @param arg4: arg4 description
    @param arg5: arg5 description
    @param arg6: arg6 description
    @return:
    """
    pass


if __name__ == "__main__":
    import qdarktheme

    def on_app_start(app):
        # this will be called after the instantiation of QApplication.
        print("app started")
        qdarktheme.setup_theme("dark")

    adapter = GUIAdapter(on_app_start=on_app_start)
    adapter.add(
        app_style_example,
        window_config=FnExecuteWindowConfig(
            output_browser_config=OutputBrowserConfig(
                stylesheet="""
                background-color: "#380C2A";
                color: "#FFFFFF";
                font-family: "Consolas";
                font-size: 12pt;
                """
            )
        ),
    )
    adapter.run()

```

<img src="../images/style_override_2.png" />

关于如何使用QSS或使用第三方库对窗口进行美化，可以参考以下文档：[界面美化：使用样式表与第三方库](adapter/style.md)

#### （二）配置窗口属性的方法

每个添加到`GUIAdapter`实例的函数都可以配置自己的窗口属性，方法是在调用`GUIAdapter.add()`时通过`window_config`参数传入`FnExecuteWindowConfig`实例。下面的示例中，分别为`function_1`和`function_2`的设置了不同的窗口属性。

> [examples/windows/fn_execute_window_config_example.py]()

```python
from pyguiadapter.adapter import GUIAdapter
from pyguiadapter.windows.fnexec import FnExecuteWindowConfig


def function_1(arg1: int, arg2: str, arg3: bool) -> None:
    pass


def function_2(arg1: int, arg2: str, arg3: bool) -> None:
    pass


if __name__ == "__main__":
    adapter = GUIAdapter()
    adapter.add(
        function_1,
        # set window config for function_1
        window_config=FnExecuteWindowConfig(
            title="Function 1", clear_checkbox_visible=True
        ),
    )
    adapter.add(
        function_2,
        # set window config for function_2
        window_config=FnExecuteWindowConfig(
            title="Function 2",
            clear_checkbox_visible=False,
            clear_checkbox_checked=False,
        ),
    )
    adapter.run()

```

<img src="../images/fn_execute_window_config_example.gif" />



#### （三）一个示例：“小窗口模式”

有时，对于一些小工具，可能并不需要那么复杂的窗口界面，甚至不用显示程序输出区域，仅仅通过弹窗的方式和用户交互即可。通过配置窗口属性，可以实现所谓“小窗口模式”。以下示例进行了如下配置：

- 隐藏了停靠窗口
- 隐藏了清除输出按钮和清除输出选框
- 改变了窗口尺寸
- 改变了窗口标题
- 改变了窗口图标
- 改变了默认参数分组的名称
- 关闭了`print_function_result`、`print_function_error`
- 启用了`show_function_result`
- 修改了`function_result_message`
- 修改了执行按钮的文字
- ......

<img src="../images/tiny_window_example.png" />

> [examples/windows/tiny_window_example.py]()

```python
from typing import Optional

from pyguiadapter.adapter import GUIAdapter
from pyguiadapter.exceptions import ParameterError
from pyguiadapter.windows.fnexec import FnExecuteWindowConfig


def equation_solver(a: float, b: float, c: float) -> Optional[tuple]:
    """
    Solving Equations: ax^2 + bx + c = 0 (a,b,c ∈ R, a ≠ 0)
    @param a: a ∈ R, a ≠ 0
    @param b: b ∈ R
    @param c: c ∈ R
    @return:
    """
    if a == 0:
        raise ParameterError(parameter_name="a", message="a cannot be zero!")

    delta = b**2 - 4 * a * c
    if delta < 0:
        return None
    x1 = (-b + delta**0.5) / (2 * a)
    if delta == 0:
        return x1, x1
    x2 = (-b - delta**0.5) / (2 * a)
    return x1, x2


if __name__ == "__main__":
    window_config = FnExecuteWindowConfig(
        title="Equation Solver",
        icon="mdi6.function-variant",
        execute_button_text="Solve",
        size=(350, 450),
        document_dock_visible=False,
        output_dock_visible=False,
        clear_button_visible=False,
        clear_checkbox_visible=False,
        show_function_result=True,
        function_result_message="real roots: {}",
        default_parameter_group_name="Equation Parameters",
        print_function_error=False,
        print_function_result=False,
    )
    adapter = GUIAdapter()
    adapter.add(equation_solver, window_config=window_config)
    adapter.run()

```

<img src="../images/tiny_window_example.gif" />





### 三、监听窗口事件

开发者可以对`FnExecuteWindow`的事件进行监听并做出响应，比如在关闭窗口前向用户再次进行确认。具体方法如下：

<img src="../images/fn_execute_window_event.png" />

下面是一个简单但完整的例子：

> [examples/windows/window_event_example_2.py]()

```python
from pyguiadapter.adapter import GUIAdapter
from pyguiadapter.window import SimpleWindowStateListener
from pyguiadapter.windows.fnexec import FnExecuteWindow
from pyguiadapter.utils import messagebox


def on_window_create(window: FnExecuteWindow):
    print("on_create")


def on_window_show(window: FnExecuteWindow):
    print("on_show")


def on_window_hide(window: FnExecuteWindow):
    print("on_hide")


def on_window_close(window: FnExecuteWindow) -> bool:
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


def on_window_destroy(window: FnExecuteWindow):
    print("on_destroy")


def event_example_2():
    pass


if __name__ == "__main__":
    event_listener = SimpleWindowStateListener(
        on_create=on_window_create,
        on_show=on_window_show,
        on_hide=on_window_hide,
        on_close=on_window_close,
        on_destroy=on_window_destroy,
    )
    adapter = GUIAdapter()
    adapter.add(event_example_2, window_listener=event_listener)
    adapter.run()
```

<img src="../images/window_event_example_2.gif" />



控制台输出如下：

<img src="../images/window_event_example_2_output.png" />

> 关于窗口事件监听，这篇文档作了更为详细的说明：[监听窗口事件](windows/window_event.md)

### 四、添加工具栏和菜单栏

开发者可以为`FnExecuteWindow`添加工具栏和菜单栏。具体方法如下：

<img src="../images/fn_execute_window_add_menus_toolbar.png" />

```python
from qtpy.QtWidgets import QAction

from pyguiadapter.action import ActionConfig, Separator
from pyguiadapter.adapter import GUIAdapter
from pyguiadapter.menu import MenuConfig
from pyguiadapter.toolbar import ToolBarConfig
from pyguiadapter.windows.fnexec import FnExecuteWindow
from pyguiadapter.utils import messagebox, filedialog


def on_action_about(window: FnExecuteWindow, action: QAction):
    messagebox.show_info_message(
        parent=window,
        message="This is an example of toolbar and menu with custom actions.",
        title="About",
    )


def on_action_close(window: FnExecuteWindow, action: QAction):
    ret = messagebox.show_question_message(
        window, "Are you sure you want to quit?", buttons=messagebox.Yes | messagebox.No
    )
    if ret == messagebox.Yes:
        window.close()


def on_action_open(window: FnExecuteWindow, action: QAction):
    ret = filedialog.get_open_file(
        window,
        title="Open File",
        start_dir="./",
        filters="JSON files(*.json);;Python files(*.py);;All files(*.*)",
    )
    if not ret:
        return
    messagebox.show_info_message(window, f"File will be opened: {ret}")


def on_action_save(window: FnExecuteWindow, action: QAction):
    ret = filedialog.get_save_file(
        window,
        title="Save File",
        start_dir="./",
        filters="JSON files(*.json);;All files(*.*)",
    )
    if not ret:
        return
    messagebox.show_info_message(window, f"File will be saved: {ret}")


def on_action_auto_theme(window: FnExecuteWindow, action: QAction):
    if action.isChecked():
        messagebox.show_info_message(window, "Auto theme is selected.")


def on_action_light_theme(window: FnExecuteWindow, action: QAction):
    if action.isChecked():
        messagebox.show_info_message(window, "Light theme is selected.")


def on_action_dark_theme(window: FnExecuteWindow, action: QAction):
    if action.isChecked():
        messagebox.show_info_message(window, "Dark theme is selected.")


action_about = ActionConfig(
    text="About",
    icon="fa.info-circle",
    on_triggered=on_action_about,
)

action_open = ActionConfig(
    text="Open",
    icon="fa.folder-open",
    shortcut="Ctrl+O",
    on_triggered=on_action_open,
)

action_save = ActionConfig(
    text="Save",
    icon="fa.save",
    shortcut="Ctrl+S",
    on_triggered=on_action_save,
)

action_close = ActionConfig(
    text="Quit",
    icon="fa.close",
    shortcut="Ctrl+Q",
    on_triggered=on_action_close,
)

action_auto_them = ActionConfig(
    text="Auto",
    checkable=True,
    checked=True,
    on_toggled=on_action_auto_theme,
)

action_light_theme = ActionConfig(
    text="Light",
    checkable=True,
    on_toggled=on_action_light_theme,
)

action_dark_theme = ActionConfig(
    text="Dark",
    checkable=True,
    on_toggled=on_action_dark_theme,
)

submenu_theme = MenuConfig(
    title="Theme",
    actions=[action_auto_them, action_light_theme, action_dark_theme],
    exclusive=True,
)
menu_file = MenuConfig(
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
menu_help = MenuConfig(
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
    adapter.add(
        menu_toolbar_example,
        window_menus=[menu_file, menu_help],
        window_toolbar=ToolBarConfig(
            actions=[action_open, action_save, Separator(), action_close]
        ),
    )
    adapter.run()

```

<img src="../images/toolbar_and_menus.gif" />

关于工具栏与菜单栏，以下文档进行了更为详细的说明：

- [为窗口添加工具栏](windows/toolbar.md)
- [为窗口添加菜单栏](windows/menus.md)

### 五、主要函数接口

`FnExecuteWindow`中定义了以下函数接口，由于在`动作（Action）`回调函数或窗口事件回调函数中，开发者可以获取到当前的`FnExecuteWindow`示例，因此开发者可以在这些回调函数中使用以下接口来实现一些特殊的操作，比如：读取当前控件上的参数，将其保存到外部文件中；或者，反过来，将外部文件保存的参数设置到对应的控件上。

```python
```

