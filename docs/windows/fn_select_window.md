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
