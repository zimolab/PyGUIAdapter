## 配置函数选择窗口

### 一、简介

在开发者向`GUIAdapter`实例中添加了多个函数后，`PyGUIAdapter`将自动生成一个`函数选择窗口`，将所有已添加的函数显示出来以供用户选择。当然，开发者也可以通过如下方式，在`GUIAdapter`实例中仅添加了一个函数时依旧显示该窗口：

```python
adapter.run(show_select_window=True)
```

`函数选择窗口`主要分成三个区域：

- ①`函数列表区域`
- ②`函数文档区域`
- ③`函数选择按钮`



<img src="../images/fn_select_window_areas.png" />



函数列表区域用于显示已添加的函数，函数将以列表的形式分组显示。用户双击函数列表中被选中的条目或者点击`函数执行按钮`，即可打开对应函数的执行窗口。

> `PyGUIAdapter`支持函数分组功能，同一组别的函数将聚合在一个列表中显示。关于函数分组，可以参考这个文档：[添加多个函数-函数分组](adapter/multiple_functions.md?id=四、函数分组)



### 二、窗口配置

`函数选择窗口`的可配置选项定义在`FnSelectWindowConfig`类中。`FnSelectWindowConfig`类继承自`BaseWindowConfig`类，因此

#### （一）通用配置

| 配置项名称      | 类型                                                         | 默认值       | 说明 |
| --------------- | ------------------------------------------------------------ | ------------ | ---- |
| `title`         | `str`                                                        | ``           |      |
| `icon`          | `Union[str, Tuple[str, Union[list, dict]], QIcon, QPixmap, NoneType]` | `None`       |      |
| `size`          | `Union[Tuple[int, int], QSize]`                              | `(800, 600)` |      |
| `position`      | `Union[Tuple[int, int], NoneType]`                           | `None`       |      |
| `always_on_top` | `bool`                                                       | `False`      |      |
| `font_family`   | `Union[str, Sequence[str], NoneType]`                        | `None`       |      |
| `font_size`     | `Union[int, NoneType]`                                       | `None`       |      |
| `stylesheet`    | `Union[str, NoneType]`                                       | `None`       |      |
| `toolbar`       | `Union[pyguiadapter.action.ToolbarConfig, NoneType]`         | `None`       |      |
| `menus`         | `Union[List[Union[pyguiadapter.action.MenuConfig, pyguiadapter.action.Separator]], NoneType]` | `None`       |      |
| `on_create`     | `Union[Callable[[ForwardRef('BaseWindow')], Any], NoneType]` | `None`       |      |
| `on_close`      | `Union[Callable[[ForwardRef('BaseWindow')], bool], NoneType]` | `None`       |      |
| `on_destroy`    | `Union[Callable[[ForwardRef('BaseWindow')], Any], NoneType]` | `None`       |      |
| `on_hide`       | `Union[Callable[[ForwardRef('BaseWindow')], Any], NoneType]` | `None`       |      |
| `on_show`       | `Union[Callable[[ForwardRef('BaseWindow')], Any], NoneType]` | `None`       |      |

#### （二）`函数选择窗口`配置



