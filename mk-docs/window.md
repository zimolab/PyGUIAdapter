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



## （三）函数选择窗口（FnExecuteWindow）

> TODO



## （四）函数执行窗口（FnSelectWindow）

> TODO