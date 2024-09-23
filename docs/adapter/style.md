## 界面风格与美化

`PyGUIAdapter`的底层基于`Qt`, 所以一些适用于`Qt`的界面美化方法同样适用于`PyGUIAdapter`。

### 一、使用样式表
`PyGUIAdapter`支持开发者使用QT样式表（`QSS`）来自定义界面风格。有几种方法可以设置样式表：

1. 在`GUIAdapter`初始化时，通过`global_style`参数设置全局样式表

`GUIAdapter`的构造函数有一个`global_style`参数，用于设置全局样式表，用户可以将样式表内容或者样式表加载函数传递给该参数。

```python

```

2. 在`on_app_start()`回调中手动加载和设置样式表

### 二、使用第三方库