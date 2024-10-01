## 窗口概述

### 一、窗口基类：`BaseWindow`

`PyGUIAdapter`中的窗口基本上都继承自[`pyguiadapter.window.BaseWindow`]()类。`BaseWindow`定义了所有窗口共有的行为。

```python
@dataclasses.dataclass
class BaseWindowConfig(object):
    ...


class WindowStateListener(object):
    ...


class BaseWindow(QMainWindow):
    def __init__(
        self,
        parent: Optional[QWidget],
        config: BaseWindowConfig,
        listener: Optional[WindowStateListener] = None,
        toolbar: Optional[ToolbarConfig] = None,
        menus: Optional[List[Union[MenuConfig, Separator]]] = None,
    ):
        ...

        
    def apply_configs(self):
        ...
```

以上是`BaseWindow`的核心，它主要做了以下几件事：

- 定义了窗口的配置方式

  - `config: BaseWindowConfig`

    > 窗口的可配置选项应当定义在一个单独配置类中（该配置类应当为`dataclass`并继承自`BaseWindowConfig`）

  - `apply_configs()`

    > `BaseWindow`将在初始化阶段（构造函数中）调用`apply_configs()`方法，从而使配置选项生效

- 定义了如何监听窗口事件

  - `listener: Optional[WindowStateListener]`

    > 开发者可以通过传入`WindowStateListener`来监听相应的窗口事件

- 定义了如何创建工具栏和窗口菜单

  - `toolbar: Optional[ToolbarConfig]`

  - `menus: Optional[List[Union[MenuConfig, Separator]]]`

    > 开发者可以通过传入一组`MenuConfig`来创建具有任意嵌套层次的窗口菜单



### 二、窗口通用配置：`BaseWindowConfig`

`BaseWindowConfig`是所有窗口配置类的父类，其中定义了窗口共有的可配置属性，主要包括窗口大小、图标、位置、字体等，其具体定义如下：

```python
@dataclasses.dataclass
class BaseWindowConfig(object):
    title: str = ""
    icon: utils.IconType = None
    size: Union[Tuple[int, int], QSize] = (800, 600)
    position: Optional[Tuple[int, int]] = None
    always_on_top: bool = False
    font_family: Union[str, Sequence[str], None] = None
    font_size: Optional[int] = None
    stylesheet: Optional[str] = None
```

|   配置项名称    |                             类型                             |    默认值    |                            说明                            |
| :-------------: | :----------------------------------------------------------: | :----------: | :--------------------------------------------------------: |
|     `title`     |                            `str`                             |     `""`     |                         窗口标题。                         |
|     `icon`      | `Union[str, Tuple[str, Union[list, dict]], QIcon, QPixmap, NoneType]` |    `None`    |                         窗口图标。                         |
|     `size`      |               `Union[Tuple[int, int], PQSize]`               | `(800, 600)` |              窗口大小，默认为`800x600`大小。               |
|   `position`    |              `Union[Tuple[int, int], NoneType]`              |    `None`    | 窗口位置。默认值为`None`，意为保持系统默认，一般居中显示。 |
| `always_on_top` |                            `bool`                            |   `False`    |                     窗口是否永远置顶。                     |
|  `font_family`  |            `Union[str, Sequence[str], NoneType]`             |    `None`    |      窗口的字体系列，默认为`None`，意为保持系统默认。      |
|   `font_size`   |                    `Union[int, NoneType]`                    |    `None`    |      窗口的字体大小，默认为`None`，意为保持系统默认。      |
|  `stylesheet`   |                    `Union[str, NoneType]`                    |    `None`    |                     窗口的qss样式表。                      |



### 三、窗口状态监听：`WindowStateListener`

开发者可以通过`WindowStateListener`，对某些窗口事件进行监听，包括：

- 窗口被创建（`on_create()`）
- 窗口被显示（`on_show()`）
- 窗口被隐藏（`on_hide()`）
- 窗口将被关闭（`on_close()`）
- 窗口被销毁（`on_destroy()`）

`WindowStateListener`的具体定义如下：

```python
class WindowStateListener(object):
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

`WindowStateListener`中事件回调函数的第一个参数为发出该事件的窗口对象，在`on_close()`函数中，开发者需要返回一个`bool`值来指示是否允许关闭窗口，返回`True`时表示允许关闭窗口，返回`False`时表示不允许关闭窗口（此时窗口关闭事件将被忽略）。



### 四、窗口工具栏：`ToolbarConfig`

`BaseWindow`（及其子类）可以添加`工具栏`，开发者通过`ToolbarConfig`来配置工具栏属性及其所包含的`动作（Action）`。

下面是一个简单的添加窗口工具栏的示例，这个示例演示了如何为`函数选择窗口`添加工具栏，同时也演示了如何利用`PyGUIAdapter`提供的对话框、输入框等功能，构建功能更加完整的应用程序。



### 五、窗口菜单：`MenuConfig`

`BaseWindow`（及其子类）可以添加`窗口菜单栏`，开发者通过`MenuConfig`来配置窗口菜单。

1. [使用`MenuConfig`定义窗口菜单](windows/menu.md)
2. [使用`ActionConfig`定义`Action`](windows/action.md)