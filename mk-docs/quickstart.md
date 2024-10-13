## （一）前置条件

要使用`PyGUIAdapter`开发应用程序，需满足以下条件：

+ `Python`版本 >= `3.8`
+ 安装`PyGUIAdapter`
+ 安装Qt的绑定库之一，可选：`PyQt5`、`PyQt6`、`PySide2`、`PySide6`

## （二）安装依赖

1、安装`PyGUIAdapter`

```shell
pip install PyGUIAdapter
```

2、安装Qt的绑定库，这里以`PySide2`为例：

```shell
pip install pyside2
```

> 如果你的环境下同时安装了多个Qt绑定库，`qtpy`默认会使用`PyQt5`(如果存在的话)。可以通过环境变量`QT_API`明确指定要使用的绑定库，可以指定以下值：
>
> + `pyqt5`
> + `pyside2`
> + `pyqt6`
> + `pyside6`
>
> 可以参见[qtpy官方说明](https://github.com/spyder-ide/qtpy)。

## （三）编写代码

### 1、实现业务逻辑，并封装为函数。

```python
from typing import Optional

from pyguiadapter.adapter.uoutput import uprint
from pyguiadapter.exceptions import ParameterError


def equation_solver(a: float = 1.0, b: float = 0.0, c: float = 0.0) -> Optional[tuple]:
    """A simple equation solver for equations like:

    **ax^2 + bx + c = 0** (a, b, c ∈ **R** and a ≠ 0)

    @param a: a ∈ R and a ≠ 0
    @param b: b ∈ R
    @param c: c ∈ R
    @return:
    """
    if a == 0:
        raise ParameterError(parameter_name="a", message="a cannot be zero!")
    uprint(f"Equation:")
    uprint(f"  {a}x² + {b}x + {c} = 0")
    delta = b**2 - 4 * a * c
    if delta < 0:
        return None
    x1 = (-b + delta**0.5) / (2 * a)
    if delta == 0:
        return x1, x1
    x2 = (-b - delta**0.5) / (2 * a)
    return x1, x2

```

### 2、创建GUI界面

```python
from pyguiadapter.adapter import GUIAdapter
...
if __name__ == "__main__":
    adapter = GUIAdapter()
    adapter.add(equation_solver)
    adapter.run()
```

**完整代码如下：**

```python
from typing import Optional

from pyguiadapter.adapter import GUIAdapter
from pyguiadapter.adapter.uoutput import uprint
from pyguiadapter.exceptions import ParameterError


def equation_solver(a: float = 1.0, b: float = 0.0, c: float = 0.0) -> Optional[tuple]:
    """A simple equation solver for equations like:

    **ax^2 + bx + c = 0** (a, b, c ∈ **R** and a ≠ 0)

    @param a: a ∈ R and a ≠ 0
    @param b: b ∈ R
    @param c: c ∈ R
    @return:
    """
    if a == 0:
        raise ParameterError(parameter_name="a", message="a cannot be zero!")
    uprint(f"Equation:")
    uprint(f"  {a}x² + {b}x + {c} = 0")
    delta = b**2 - 4 * a * c
    if delta < 0:
        return None
    x1 = (-b + delta**0.5) / (2 * a)
    if delta == 0:
        return x1, x1
    x2 = (-b - delta**0.5) / (2 * a)
    return x1, x2


if __name__ == "__main__":
    adapter = GUIAdapter()
    adapter.add(equation_solver)
    adapter.run()
```

**界面效果如下：**

<div style="text-align:center">
    <img src="/assets/equation_solver.gif" />
</div>


## （四）一些说明

### 1、原理
在`PyGUIAdapter`中，函数是界面的基本单元，一个函数对应了一个窗口，函数的参数列表则定义了窗口中的控件。

在基于“`输入（Input）-处理（Process）-输出（Output）`”的程序设计模型中，`PyGUIAdapter`为开发者自动完成了“`输入（Input）`”和“`输出（Output）`”这两个环节。因此，在绝大多数情况下，开发者唯一需要关注的就是如何实现“`处理（Process）`”环节，也就是实现程序的核心功能或者说业务逻辑。

与传统GUI编程不同，在使用`PyGUIAdapter`时，GUI创建和管理的整个过程对于开发者而言几乎是透明的，开发者基本上不会感知到这一过程的存在，这意味着，开发者不会被`“如何创建窗口和控件”`、`“如何选择和布局控件”`、`“如何处理用户输入数据”`、`“如何响应事件”`之类细枝末节的问题分散注意力，从而将关注点始终聚焦在核心功能的实现上。

将界面与逻辑进行分离被认为是一种好实践，`PyGUIAdapter`这种设计模式进一步探索了界面与逻辑分离的可能性。 那么，`PyGUIAdapter`是如何做到这一点的呢？`PyGUIAdapter`的实现实际上并不复杂，没有使用所谓的“黑魔法”，全部基1于Python的基本特性，主要包括：

- **类型注解（type hint）**
- **内醒与反射机制（inspect）**
- **文档字符串（docstring）**

在运行时，`PyGUIAdapter`会获取函数参数列表，并根据参数的类型、默认值等，自动选择最合适控件。
> 例如：对于`int`类型的参数，将默认创建`IntSpinBox`；对于`str`类型的参数，将默认创建`LineEdit`等。 

同时，`PyGUIAdapter`还将从函数的签名、文档字符串等处，充分挖掘函数的信息，并基于此自完成窗口创建、界面布局和事件绑定等工作。当用户点击`Execute`按钮时，`PyGUIAdapter`将从控件中收集用户输入数据，并对这些数据进行必要转换和处理，之后，将其作为对应参数调用函数，获取函数调用的结果并处理可能发生的异常。

> `PyGUIAdapter`充分利用了Python的类型注解机制。在`PyGUIAdapter`中，函数参数的类型注解不是可有可无的，它是生成参数控件的决定因素之一。
> 虽然并非说不使用类型注解就完全无法利用`PyGUIAdapter`——`PyGUIAdapter`也允许开发者手动为每个参数显式地指定控件——但是，这样会在很大程度上会失去使用`PyGUIAdapter`的意义。所以，**强烈建议开发者养成使用类型注解的习惯。**。

### 2、参数校验与异常处理

程序运行时的错误或者异常，很多时候根源在于`未经校验的用户输入`。在编写程序时，不要做一个乐观主义者，总是抱着“用户会按照预想的方式使用我的程序”将会成为混乱之始，要多想想那些**“最坏”**的情况，也就是所谓的**“边界条件”**。**“永远不要相信用户的输入”**可以避免很多问题（或者说绝大部分问题），对用户输入进行校验，尽可能过滤那些“非法”的值是增强程序健壮性的关键所在。 

因此，`PyGUIAdapter`不仅鼓励开发者对函数参数（也就是用户输入）进行校验，并且为此提供了一种简单且符合直觉的处理机制。 在上述的示例代码中，有这样几行代码，展示了参数校验的基本方式：
```python
    ...
    if a == 0:
        raise ParameterError(parameter_name="a", message="a cannot be zero!")
    ...
```

对于非法的函数参数值，开发者只需抛出`ParameterError`异常，即完成了参数的校验工作。`PyGUIAdapter`将自动完成的后续的工作，以合适的方式提醒用户，函数的某个参数输入了一个不合适的值。

<div style="text-align: center">
    <img src="/assets/handle_parameter_error.gif" />
</div>

事实上，`PyGUIAdapter`对于`ParameterError`的处理是更为一般的异常处理机制的一个特例。尽管`PyGUIAdapter`鼓励开发者尽可能预见程序可能发生的异常并提前规避它们，但客观上看程序的异常是无法完全消除的。对于函数中发生的异常，`PyGUIAdapter`的默认策略是：**捕获它们，弹窗提醒用户，并在程序输出区域打印出异常信息。** 这样的设计主要是**为了增强程序的`健壮性`，防止未捕获的异常导致整个程序崩溃**。


### 3、描述性信息

无论是命令行程序还是图形界面程序，为程序及其参数提供描述性文字都是非常有必要的一件事。这些文字一般被称为程序的**帮助信息**，对于`CLI`程序，一般使用`-h`或`--help`来获取其帮助信息，例如，下图是`pyhton -h`命令打印出的`Python`解释器程序的部分帮助信息。

<div style="text-align: center">
    <img src="/assets/cli_help.png" />
</div>

`PyGUIAdapter`同样支持为函数参数以及函数本身添加描述信息。

对于函数参数，`PyGUIAdapter`在其输入控件的上方预留了用于显示描述信息的空间：

<div style="text-align: center">
    <img src="/assets/parameter_description.png" />
</div>

对于函数本身，`PyGUIAdapter`则提供了专门的`文档浏览器（Document Browser）`来展示其说明信息：

<div style="text-align: center">
    <img src="/assets/function_description.png" />
</div>

回看示例代码，似乎并没有通过特殊的方法添加这些信息，那么这些信息从何而来呢？仔细阅读代码，不难发现，这些信息实际上来自于函数的`文档字符串（docstring）`。



<div style="text-align: center">
    <img src="/assets/gui_description.png" />
</div>



**“尽可能利用现有信息，降低开发者的学习和使用成本”**是`PyGUIAdapter`的重要设计思想，因此它会自动从函数的`docstring`中提取函数和参数的描述信息，并将其显示在界面的正确位置。当然，这也要求开发者尽可能规范地编写函数的说明文档，考虑到不同的开发者可能习惯于不同的文档格式，`PyGUIAdapter`对多种常用的文档格式进行了支持，包括：

-  `ReST`
- `Google`
- `Numpydoc-style` 
- `Epydoc` 

> 除了从函数的`docstring`中提取函数及其参数的描述信息，`PyGUIAdapter`也允许开发者手动设置这些信息，这对于描述信息太长或者需要国际化的场合尤其有用。可以从以下文档获取具体的说明：
>
> - 关于如何手动设置参数的描述信息，参见：[配置控件属性](widget-config.md)。
> - 关于如何手动设置函数的描述信息（文档），参见：[添加多个函数](multiple-functions.md)。

### 4、打印消息

`print()`是Python开发者非常熟悉的一个函数，常被用于向用户展示程序运行信息。一般情况下，通过`print()`打印的信息会被输出到程序的标准输出上，为了使开发者能够将信息打印到窗口的`输出浏览器（Output Browser）`，`PyGUIAdapter`提供了`uprint()`函数。

> 可以通过以下方式导入`uprint()`函数：
> ```python
> from pyguiadapter.adapter.ucontext import uprint
> ```
> 或者，从`pyguiadapter.adapter.uoutput`导入：
> ```python
> from pyguiadapter.adapter.uoutput import uprint
> ```

`uprint()`函数的用法基本上同内置函数`print()`保持一致，其原型如下：

::: pyguiadapter.adapter.ucontext.uprint
    options:
        heading_level: 4
        show_source: false
        show_root_full_path: false

> 如其原型所示，`uprint()`支持输出`html`格式的富文本内容，比如图片。但需要指出的是，`输出浏览器`对于`html`的支持是有限的，具体可以参考QT的官方文档：[Supported HTML Subset](https://doc.qt.io/qtforpython-5/overviews/richtext-html-subset.html)


除了`uprint()`，`pyguiadapter.adapter.uoutput`中还提供了一些其他输出信息的方法。借助这些方法，开发者可以输出格式更加丰富的内容，可以查看以下文档获取更多信息：

[pyguiadapter.adapter.uoutput](apis/pyguiadapter.adapter.uoutput.md)

