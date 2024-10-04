## 函数执行窗口（FnExecuteWindow）

### 一、简介

`函数执行窗口（FnExecuteWindow）`是用户与程序进行交互的主要界面。一个典型的`函数执行窗口（FnExecuteWindow）`由以下几个部分组成：

<img src="../images/solver.png" />

包括一个固定区域（`Parameters Area`）和两个停靠窗口（`Document Dock`和`Output Dock`）。

1. **参数控件区（Parameters Area）**：主要用于放置函数参数控件。

2. **函数文档停靠窗口（Document Dock）**：主要用于显示函数的文档信息。默认情况下，其内容来源于函数的`文档字符串（docstring）`。

3. **程序输出停靠窗口（Output Dock）**：主要用于显示程序的输出信息。默认情况下，函数的返回值、函数调用过程中发生的异常信息均会显示在此区域。

### 二、配置窗口属性

#### （一）简介

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
|    `document_browser_config`     |               `Optional[OutputBrowserConfig]`                |               `None`                |                    函数文档浏览器的配置。                    |
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
|                                  |                                                              |                                     |                                                              |

#### （二）配置窗口属性的方法



#### （三）一些示例

##### 1、小窗口模式

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

### 四、添加工具栏

### 五、添加菜单栏

### 六、主要函数接口

