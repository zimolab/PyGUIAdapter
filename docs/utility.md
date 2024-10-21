## （一）概述

`PyGUIAdapter`提供了大量实用函数，开发者可以在窗口或`Action`的事件回调函数中调用这些函数，进一步扩展程序的功能。

这些函数可以在[`pyguiadapter.utils`]({{main_branch}}/pyguiadapter/utils/)包下找到，主要包含以下几个模块：

- [`filedialog`]({{main_branch}}/pyguiadapter/utils/filedialog.py)，主要提供文件选择对话框功能。
- [`messagebox`]({{main_branch}}/pyguiadapter/utils/messagebox.py)，主要提供消息对话框功能。
- [`inputdialog`]({{main_branch}}/pyguiadapter/utils/inputdialog.py)，主要提供输入对话框功能。

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
