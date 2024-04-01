# PyGUIAdapter

---

### 中文 | [English](./README.md)

一个可以轻松将（几乎）任意Python函数转换为GUI应用的库。

![PyGUIAdapter](./screenshoots/pyguiadapter_mid.png)

一个真实的应用案例：[Simple-OTP](https://github.com/zimolab/simple-otp)

---

## 1. 快速开始

### 1.1 安装

使用pip安装：

```bash
pip install pyguiadapter
```

使用poetry安装：

```bash
poetry add pyguiadapter
```

### 1.2 简单用法

要将你的python函数转换为GUI应用是一件非常简单的事情，只需几行代码。


(1) 首先准备一个函数，使用python的类型注解语法，标注好每个参数的类型。 

比如你有下面这么一个函数（不用管它的具体功能，仅关注其参数是如何定义的）：

```python
import os.path


def create_file(path: str, filename: str, content: str, overwrite: bool = False):
    path = os.path.join(path, filename)
    if not os.path.isfile(path) or overwrite:
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
            return True
    return False
```

(2) 创建GUIAdapter实例，将你的函数添加到该实例中：

```python
from pyguiadapter.adapter.adapter import GUIAdapter

gui_adapter = GUIAdapter()
gui_adapter.add(create_file)
```

(3) 调用`GUIAdapter.run()`方法，即可运行GUI应用。

```python
gui_adapter.run()
```

完整代码如下：

```python
import os.path


def create_file(path: str, filename: str, content: str, overwrite: bool = False):
    path = os.path.join(path, filename)
    if not os.path.isfile(path) or overwrite:
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
            return True
    return False


if __name__ == "__main__":
    from pyguiadapter.adapter.adapter import GUIAdapter

    gui_adapter = GUIAdapter()
    gui_adapter.add(create_file)
    gui_adapter.run()
```

上述代码的运行结果如下：

![create_file_demo](./screenshoots/create_file_demo.png)

可以看到，简简单单3行代码就将一个`create_file()`函数转换为了一个GUI应用，GUIAdapter为函数的每个参数都创建了对应GUI控件，
通过这些控件，用户可以输入参数的值，然后点击`Execute`按钮即可使用这些参数调用函数。 而在正是PyGUIAdapter的工作方式，用户向其添加一个函数，
它会自动分析这个函数，并根据一定的规则，为这个函数的每个参数创建对应的GUI控件， 一般情况下，GUIAdapter会根据参数的类型决定其所对应的GUI控件的类型，
比如上面的`create_file()`函数中，前三个参数都是字符串类型， 因此GUIAdapter会为这些参数都创建单行文本框，而最后一个参数是布尔类型，
因此GUIAdapter为它创建了一个复选框。

到这里，你已经了解了PyGUIAdapter的基本用法，需要注意的是，PyGUIAdapter在设计时就非常注重灵活性和可扩展性，
它有许多可以自定义的东西，比如你可以自定义函数参数控件的类型及其属性，你也可以自定义窗口的图标、标题、大小、样式等等。
如果内置的控件无法满足你的需求， 你还可以自定义控件，然后像使用内置控件那样使用它。

---

## 2. 例子和文档

为了展示PyGUIAdapter的用法，我编写了许多示例，这些示例写的非常简单，几乎每个示例，都只演示了PyGUIAdapter的一个特性，
这些示例可以帮助你更好的理解PyGUIAdapter的用法。

### 2.1 示例代码

这些示例存放在以下目录中：[examples](./examples)

可以直接运行这些示例，查看相应的效果。

### 2.2 文档

更多的文档可以在这里找到：[docs/](./docs)

目前文档还在编写中，后续会陆续更新，现阶段请使用者主要通过例子来进行学习。

---

## 3. 支持的参数类型及一些限制

文档的开头说过，PyGUIAdapter支持将**几乎**任意python函数转换为GUI应用，但是也存在一些限制。

### 3.1 不支持仅位置参数（Positional-Only Argument）

函数的参数列表中不能包含**仅位置参数（Positional-Only Argument）**，仅位置参数是python3.8引入的新特性（PEP 570），它长下面这样：

```python
def f(positional_argument, /, positional_or_keyword_argument, *, c):
    pass

#positional_argument                    位置参数
#positional_or_keyword_argument         位置参数和关键字参数
#keyword_argument                       关键字参数
```

不过，从实际的代码来看，**仅位置参数（Positional-Only Argument）** 并不常用

### 3.3 不支持内置函数

不支持内置函数，如`open`。当然，一般也不会直接有为内置函数生成GUI界面的需求，如果非要这么做，解决方案也很简单，写一个函数将内置函数的封装一下就行啦。


### 3.4 支持有限的参数类型

PyGUIAdapter原生支持的参数类型包括：`int`、`float`、`bool`、`str`、`list`、`tuple`、`dict`，几乎涵盖了绝大多数需求。

PyGUIAdapter为这些参数提供了丰富的GUI控件，具体可以参见`function2widgets`库，也可以查看`examples`下的例子。

> function2widgets是PyGUIAdapter的基础设施，它是我为了PyGUIAdapter写的一个独立的库，它提供了全部内置参数控件类型

当然，如果你非要支持一些更为复杂的自定义类型，也是可以实现的，而且并不复杂， 比如你需要支持一个`2DPoint`类型，那么你可以通过以下步骤实现：

首先，需要为`2DPoint`类型创建一个GUI控件，比如一个带两个数字输入框的控件，具体的实现可以参考内置控件，
比如`function2widgets.widgets.lineedit.IntLineEdit`，比如下面这个样子：

```python
from function2widgets.widget import BaseParameterWidget

class Point2DInput(BaseParameterWidget):
    # 实现必要的接口和相应的逻辑
    ...

```


接下来，你需要将`Point2DInput`注册到参数控件工厂中，代码可能长下面这样：

```python
from pyguiadapter.commons import get_widget_factory

factory = get_widget_factory()
factory.register("2DPointInput", Point2DInput)
```

最后，关键的一步，就是让PyGUIAdapter知道如何哪个参数应该使用`Point2DInput`控件，这涉及到自定义参数控件的内容，有多种方法可以做到，
这里简单介绍其中一种，即在调`add()`函数时，传入`widget_configs`参数，代码可能长下面这样：

```python
gui_adapter.add(some_func, widget_configs={"position": {"type": "2DPointInput"}})
```

这样，PyGUIAdapter就会为`position`参数创建`Point2DInput`控件了。

---

## 4. PyGUIAdapter是什么

PyGUIAdapter是一个用于将函数转换为GUI应用的库，很多时候我们需要将python程序交付给其他人使用，其中一种方式是将这些程序做成命令行的形式，
但不可否认，很多时候我们也有创建GUI应用界面的需求，毕竟不是每个人都擅长使用命令行（尽管就我个人来说，命令行确实好用且使用上实际更加高效）。
然而，创建GUI代码是耗时、麻烦且无趣，而且对于不熟悉GUI开发的程序员来说，他们还需要临时学习一种GUI框架，这无疑增添了许多额外的学习成本，
因此，PyGUIAdapter应运而生。PyGUIAdapter可以使程序员专注于功能实现，创建界面几乎不会带了额外的心智负担，当一个功能函数实现了，那边基本上 也意味着
GUI界面也已经实现，最多也就是再做一些自定义，控件的创建和布局、事件的处理这些琐碎的事情，PyGUIAdapter已经帮你处理好了。

PyGUIAdapter可以使GUI应用程序创建和命令行程序的开发一样简单，甚至更加简单。

---

## 5. PyGUIAdapter不适合什么

那些需要复杂界面交互或者界面具有复杂状态的场景，PyGUIAdapter可能不太适合。

## 6. PyGUIAdapter背后的技术

为了实现PyGUIAdapter，我创建了[function2widgets](https://github.com/zimolab/function2widgets)， 正如它名字所暗示的那样，
它的核心功能就是从给定给定函数中提取信息，然后基于一定规则，将这些信息转换为GUI控件。 而function2widgets的底层，则是基于PyQt6这个流行的GUI框架。

## 7. 待实现或完善的功能

目前，PyGUIAdapter已经实现了大部分核心的功能，但是由于本人本职工作与写代码无关，这个项目（包括function2widgets）也仅仅是我花了一周业余时间写出来的，
所以很多功能可能还不是很完善，代码也可能还存在许多bug，如果有需要，欢迎提issue。

接下来，需要实现或完善的功能有：
1. i18n
2. 更多内置的参数控件类型（比如颜色控件、时间日期控件、文件拖放控件等等）
3. 更完善的示例代码
4. 更完善的文档
5. 更多可hook的事件
6. 增强从用户代码访问底层控件和窗口的能力
7. 用户自定义菜单
8. 优化的布局
9. 稳定的API接口
10. 其他

## 8. 注意事项

由于PyGUIAdapter还在开发和快速迭代阶段，所以目前的API接口可能会有所变化。

## 9. 其他

如果这个库对您有帮助，欢迎给个star，谢谢！

