## 使用`ActionConfig`定义`Action`

在`PyGUIAdapter`中，`ActionConfig`用于配置工具栏或菜单栏上的`动作（Action）`。

> `ActionConfig`在[`pyguiadapter.action`]()模块中定义。

所谓的”`动作（Action）`“，在工具栏上表现为一个个可以点击的动作按钮，在菜单栏上则表现为菜单项。它具有以下属性：

```python
@dataclasses.dataclass
class ActionConfig(object):
    text: str
    on_triggered: Optional[ActionCallback] = None
    on_toggled: Optional[ActionCallback] = None
    icon: IconType = None
    icon_text: Optional[str] = None
    auto_repeat: bool = False
    enabled: bool = True
    checkable: bool = False
    checked: bool = False
    shortcut: Optional[str] = None
    shortcut_context: Optional[Qt.ShortcutContext] = None
    tooltip: Optional[str] = None
    whats_this: Optional[str] = None
    status_tip: Optional[str] = None
    priority: Optional[QAction.Priority] = None
    menu_role: Optional[QAction.MenuRole] = None
```

> `ActionConfig`、`ActionCallback`均在在[`pyguiadapter.action`]()模块中定义。
>
> `ActionCallback`实际上是一个类型别名：
>
> ```python
> ActionCallback = Callable[[ForwardRef("BaseWindow"), QAction], None]
> ```
>
> 其具体含义是：具有两个参数，第一个参数为`BaseWindow`类型（或其子类），第二个参数为`QAction`，无返回值的函数。比如，以下函数就符合`ActionCallback`的要求：
>
> ```python
> def on_action_xxx(window: FnSelectWindow, action: QAction)：
> 	pass
> ```

实际上，`ActionConfig`就是简单集合了`QAction`的属性，其中最常用的属性包括：

- `text`：Action的文本
- `icon`：Action的图标
- `shortcut`：Action的快捷键
- `on_triggered`：Action被触发（比如被单击或对应快捷键按下）时的回调函数
- `on_toggled`：Action的check状态发生变化时的回调函数
- `checkable`：Action是否为可选择/可勾选的，若该属性为`True`，则Action的行为将变得类似于一个CheckBox，具有`选择`、`未选中`二元状态，此时开发者可以在`on_toggled`回调函数中监听到这种状态变化。
- `checked`：Action是否未选中状态，仅在`checkable`为`True`时生效。

其他属性，可以参考Qt的官方文档：[Synopsis - Qt for Python](https://doc.qt.io/qtforpython-6/PySide6/QtGui/QAction.html#PySide6.QtGui.QAction.autoRepeat)