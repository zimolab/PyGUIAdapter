## 窗口概述

### 一、窗口父类：`BaseWindow`

#### （一）简介

`PyGUIAdapter`中主要有两种类型的窗口：`函数选择窗口（FnSelectWindow）`和`函数执行窗口（FnExecuteWindow）`，它们都继承自[`pyguiadapter.window.BaseWindow`]()类。窗口父类`BaseWindow`定义了子类窗口的总体外观和某些共同行为，比如：

- 开发者可以使用`窗口配置类`配置窗口的某些属性
- 开发者可以向窗口中添加工具栏和菜单栏
- 开发者可以监听窗口的某些事件
- 开发者可以在窗口事件回调中获取/改变添加到工具栏（菜单栏）中的`动作（Action）`的状态
- ......

#### （二）主要接口

父类`BaseWindow`中定义并实现了一些基本的接口，开发者可以在`动作（Action）`或窗口事件的回调函数中调用这些接口。

##### 1、`动作（Action）`相关

以下接口主要用于查找或改变窗口工具栏（菜单栏）中`动作（Action）`的状态。

```python
class BaseWindow(QMainWindow):
    def find_action(self, action_config: ActionConfig) -> Optional[QAction]:
        ...

    def set_action_state(self, action_config: ActionConfig, checked: bool) -> bool:
        ...

    def toggle_action_state(self, action_config: ActionConfig) -> bool:
        ...

    def query_action_state(self, action_config: ActionConfig) -> Optional[bool]:
        ...
```

##### 2、窗口属性相关

以下接口主要用于设置或获取窗口的某些属性，包括标题、图标、大小、位置、字体、样式、是否置顶等。

```python
class BaseWindow(QMainWindow):
    def set_title(self, title: str):
        ...

    def get_title(self) -> str:
        ...

    def set_icon(self, icon: IconType):
        ...

    def set_always_on_top(self, enabled: bool):
        ...

    def is_always_on_top(self) -> bool:
        ...

    def set_size(self, size: Union[Tuple[int, int], QSize]):
        ...

    def get_size(self) -> Tuple[int, int]:
        ...

    def set_position(self, position: Optional[Tuple[int, int]]):
        ...

    def get_position(self) -> Tuple[int, int]:
        ...

    def set_font(self, font_family: Union[str, Sequence[str]], font_size: int):
        ...

    def get_font_size(self) -> int:
        ...

    def get_font_family(self) -> str:
        ...

    def get_font_families(self) -> Sequence[str]:
        ...

    def set_stylesheet(self, stylesheet: Optional[str]):
        ...

    def get_stylesheet(self) -> str:
        ...
```



#### （三）主要子类

`BaseWindow`的主要子类有：

- `FnSelectWindow`，即`函数选择窗口`。
- `FnExecuteWindow`，即`函数执行窗口`。



### 二、窗口配置父类：`BaseWindowConfig`

#### （一）窗口共有的可配置属性

`窗口配置类`用于配置窗口属性。`BaseWindowConfig`是所有窗口配置类的父类，它定义了`BaseWindow`子类窗口共有的属性，包括窗口大小、图标、位置、字体等，其具体定义及含义如下：

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

#### （二）主要子类

`BaseWindowConfig`的主要子类包括：

- `FnSelectWindowConfig`，用于配置`函数选择窗口（FnSelectWindowConfig）`。
- `FnExecuteWindowConfig`，用于配置`函数执行窗口（FnExecuteWindowConfig）`。
