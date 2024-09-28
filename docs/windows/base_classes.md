## `BaseWindow` 与 `BaseWindowConfig`

### 一、窗口基类：`BaseWindow`

`PyGUIAdapter`中的窗口基本上都是[`pyguiadapter.window.BaseWindow`]()的子类。`BaseWindow`定义了所有子类窗口共有的行为模式。比如，它规定了窗口的可配置属性应当定义在对应的配置类中

### 二、窗口配置基类：`BaseWindowConfig`