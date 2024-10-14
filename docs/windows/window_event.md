## 监听窗口事件

### 一、窗口事件监听器：`BaseWindowStateListener`
开发者可对窗口事件进行监听，主要包括以下事件：

- 窗口被创建（`on_create()`）
- 窗口被显示（`on_show()`）
- 窗口被隐藏（`on_hide()`）
- 窗口将被关闭（`on_close()`）
- 窗口被销毁（`on_destroy()`）

`BaseWindowStateListener`是实现窗口事件监听的核心组件，其具体定义如下：

```python
class BaseWindowStateListener(object):
    def on_create(self, window: "BaseWindow"):
        pass

    def on_close(self, window: "BaseWindow") -> bool:
        return True

    def on_destroy(self, window: "BaseWindow"):
        pass

    def on_hide(self, window: "BaseWindow"):
        pass

    def on_show(self, window: "BaseWindow"):
        pass

```

在`BaseWindowStateListener`中，事件回调函数的第一个参数为发出该事件的窗口对象。除`on_close()`回调函数外，其余回调函数均无返回值。

在`on_close()`回调函数中，开发者需要返回一个`bool`值来指示是否允许关闭窗口：

- 返回`True`表示允许关闭窗口；
- 返回`False`表示不允许关闭窗口，此时窗口关闭事件将被忽略。

### 二、监听窗口事件方法之一：子类化`BaseWindowStateListener`
开发者可以继承`BaseWindowStateListener`并重事件回调函数，以实现对特定事件的监听。例如，下面的例子演示了如何为`函数执行窗口（FnExecuteWindow）`添加事件监听器。下面是一个简单的示例：

> [examples/windows/window_event_example_1.py]()

```python
from pyguiadapter.adapter import GUIAdapter
from pyguiadapter.window import BaseWindowEventListener
from pyguiadapter.windows.fnexec import FnExecuteWindow
from pyguiadapter.utils import messagebox


def event_example_1():
    pass


class ExampleEventListener(BaseWindowEventListener):

    def on_create(self, window: FnExecuteWindow):
        print("on_create")
        super().on_create(window)

    def on_close(self, window: FnExecuteWindow) -> bool:
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

    def on_destroy(self, window: FnExecuteWindow):
        print("on_destroy")
        super().on_destroy(window)

    def on_hide(self, window: FnExecuteWindow):
        print("on_hide")
        super().on_hide(window)

    def on_show(self, window: FnExecuteWindow):
        print("on_show")
        super().on_show(window)


if __name__ == "__main__":
    event_listener = ExampleEventListener()
    adapter = GUIAdapter()
    adapter.add(event_example_1, window_listener=event_listener)
    adapter.run()

```

<img src="../images/window_event_example_1.gif" />

### 二、监听窗口事件方法之二：使用`SimpleWindowStateListener`

对于偏爱函数而非子类化的开发者，`PyGUIAdapter`也提供了另外一种创建窗口事件监听器的方法。下面是一个简单的示例：

> [examples/windows/window_event_example_2.py]()

```python
from pyguiadapter.adapter import GUIAdapter
from pyguiadapter.window import SimpleWindowEventListener
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
    event_listener = SimpleWindowEventListener(
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

<img src="G:/Projects/PyGUIAdapter/docs/images/window_event_example_2_output.png" />

---

上面的例子均以`函数执行窗口（FnExecuteWindow）`为例，`函数选择窗口（FnSelectWindow）`作为`BaseWindow`的子类，开发者同样也可以为其设置事件监听器，方法是在调用`adapter.run()`时指定`select_window_listener`参数，下面是一个简单的示例：

> [examples/windows/window_event_example_3.py]()

```python
from pyguiadapter.adapter import GUIAdapter
from pyguiadapter.window import SimpleWindowEventListener
from pyguiadapter.utils import messagebox
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

