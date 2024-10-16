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

> `uprint()`支持输出`html`格式的富文本内容，比如图片。但需要指出的是，`输出浏览器`对于`html`的支持是有限的，具体可以参考QT的官方文档：[Supported HTML Subset](https://doc.qt.io/qtforpython-5/overviews/richtext-html-subset.html)



除了`uprint()`，`pyguiadapter.adapter.uoutput`还实现了许多用于输出信息的函数，借助这些函数，开发者可以输出格式更加丰富的内容，可以查看以下文档获取更多信息：[pyguiadapter.adapter.uoutput](apis/pyguiadapter.adapter.uoutput.md)


## （五）、示例进阶

`PyGUIAdapter`的高度灵活性体现在允许开发者对生成的界面进行配置，开发者不仅可以配置窗口的属性和外观，而且可以对函数每个参数对应的控件进行精细化的调整，改变其默认的行为。

下面，将逐步完善上述示例代码，并在此过程中演示配置窗口和控件属性的方法。 

### 1、配置窗口属性

首先，我们将对示例程序的窗口进行配置，包括：



+ 调整窗口大小
+ 设置窗口标题和图标
+ 隐藏`文档浏览器`
+ 改变函数返回值的消息格式
+ 弹出对话框显示函数返回值
+  ......

对窗口属性的调整需要借助`窗口配置类`对象。对于函数执行窗口，其窗口配置类为`FnExecuteWindowConfig`，该类中定义了函数执行窗口的可配置属性，开发者可以通过以下方式对窗口进行配置：

<div style="text-align: center">
    <img src="/assets/how_to_config_exec_win.png" />
</div>

完整代码如下：

```python
from typing import Optional

from pyguiadapter.adapter import GUIAdapter
from pyguiadapter.adapter.uoutput import uprint
from pyguiadapter.exceptions import ParameterError
from pyguiadapter.windows.fnexec import FnExecuteWindowConfig


def equation_solver_2(
    a: float = 1.0, b: float = 0.0, c: float = 0.0
) -> Optional[tuple]:
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
    window_config = FnExecuteWindowConfig(
        title="Equation Solver",
        icon="mdi6.function-variant",
        execute_button_text="Solve",
        size=(350, 550),
        document_dock_visible=False,
        output_dock_initial_size=(None, 100),
        show_function_result=True,
        function_result_message="roots: {}",
        default_parameter_group_name="Equation Parameters",
    )

    adapter = GUIAdapter()
    adapter.add(equation_solver_2, window_config=window_config)
    adapter.run()

```

效果如下：

<div style="text-align: center">
    <img src="/assets/how_to_config_exec_win_result.png" />
</div>

> `FnExecuteWindowConfig`定义了大量可配置属性，这里仅仅演示了其中一小部分，开发者可以参考以下文档获取完整的可配置属性列表：[pyguiadapter.windows.fnexec.FnExecuteWindowConfig](apis/pyguiadapter.windows.fnexec.md#FnExecuteWindowConfig)



###  2、配置控件属性

在目前的示例程序中，参数`a`、`b`、`c`的输入控件只能输入小数点后2位，且每次调整的步进值为1。

<div style="text-align: center">
    <img src="/assets/widget_config_before.gif" />
</div>



原因在于`float`类型对应的`FloatSpinBox`控件，其`step`（单次步进值）属性和`decimals`（小数点位数）属性分别被配置为`1.0`和`2`。开发者可以通过多种方式修改控件的默认属性配置，以达到改变控件的默认行为的目的。

<div style="text-align: center">
    <img src="/assets/floatspin_def_config.png" />
</div>

现在我们将对上述示例做进一步修改，将参数`a`、`b`、`c`对应控件的`decimals`（小数点位数）配置为`5`，`step`（单次步进值）配置为`0.00005`。

#### 方法1：利用`@params...@end`配置块

开发者可以在函数的`docstring`中配置参数的控件。`PyGUIAdapter`将`docstring`中使用`@params`和`@end`包裹起来文本块视为控件的配置块。开发者可以在该区域对控件的属性进行配置。配置块的格式为`TOML`。可以使用如下格式配置指定控件的指定属性：

```toml
[参数名称]
属性名称1 = 属性值1
属性名称2 = 属性值2
属性名称N = 属性值N
```

比如要配置上述示例中参数`a`、`b`、`c`对应控件的`step`属性和`decimals`属性，可以这样做：

<div style="text-align: center">
    <img src="/assets/params_config_block.png" />
</div>

**完整代码如下：**

```python
from typing import Optional

from pyguiadapter.adapter import GUIAdapter
from pyguiadapter.adapter.uoutput import uprint
from pyguiadapter.exceptions import ParameterError
from pyguiadapter.windows.fnexec import FnExecuteWindowConfig


def equation_solver_3(
    a: float = 1.0, b: float = 0.0, c: float = 0.0
) -> Optional[tuple]:
    """A simple equation solver for equations like:

    **ax^2 + bx + c = 0** (a, b, c ∈ **R** and a ≠ 0)

    @param a: a ∈ R and a ≠ 0
    @param b: b ∈ R
    @param c: c ∈ R
    @return:

    @params
    [a]
    decimals = 5
    step = 0.00005

    [b]
    decimals = 5
    step = 0.00005

    [c]
    decimals = 5
    step = 0.00005
    @end

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
    window_config = FnExecuteWindowConfig(
        title="Equation Solver",
        icon="mdi6.function-variant",
        execute_button_text="Solve",
        size=(350, 550),
        document_dock_visible=False,
        output_dock_initial_size=(None, 100),
        show_function_result=True,
        function_result_message="roots: {}",
        default_parameter_group_name="Equation Parameters",
    )

    adapter = GUIAdapter()
    adapter.add(equation_solver_3, window_config=window_config)
    adapter.run()

```

#### 方法2：使用配置类对象

在`@params...@end`块中配置参数的控件，优点是简单、快速，但也并非万能。一方面，由于配置块的格式为`TOML`，其支持的数据类型有限，某些控件的一些属性可能使用了超出其表达能力范围的数据类型；另一方面，如果要配置的参数很多，或者要设置的属性很多，可能会使`docstring`变得非常冗长。在`docstring`中编写参数配置代码也将失去现代`IDE`或者代码编辑所带来种种便利，比如代码提示、自动完成等。

总之，在`@params...@end`中配置控件参数是一种很便捷的手段，但也无法解决所有的问题，因此，`PyGUIAdapter`提供了另一种更加通用的配置控件属性的方法，那就是使用控件的配置类对象（实际上，在`@params...@end`中编写配置，最终也会被转换为对应的配置类对象）。

在`PyGUIAdapter`，函数参数的控件，其类型一般由参数的数据类型决定，而控件的属性，则由其对应的配置类定义。比如：

- `int` -> `IntSpinBox`  -> `IntSpinBoxConfig`

- `float` -> `FloatSpinBox` -> `FloatSpinBox`
- `str` -> `LineEdit` -> `LineEditConfig`
- ......

确定了参数对应控件的类型，便可以创建对应配置类对象来对其属性进行配置，以上述示例代码为例，可以这样配置其属性：

> 使用配置类对象时，开发者在函数签名中指定的参数的默认值将会被覆盖，可以通过配置类对象的`default_value`属性重新指定

<div style="text-align: center">
    <img src="/assets/widget_config_class_demo.png" />
</div>

**完整代码如下**

```python
from typing import Optional

from pyguiadapter.adapter import GUIAdapter
from pyguiadapter.adapter.uoutput import uprint
from pyguiadapter.exceptions import ParameterError
from pyguiadapter.widgets import FloatSpinBoxConfig
from pyguiadapter.windows.fnexec import FnExecuteWindowConfig


def equation_solver_4(
    a: float = 1.0, b: float = 0.0, c: float = 0.0
) -> Optional[tuple]:
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
    window_config = FnExecuteWindowConfig(
        title="Equation Solver",
        icon="mdi6.function-variant",
        execute_button_text="Solve",
        size=(350, 550),
        document_dock_visible=False,
        output_dock_initial_size=(None, 100),
        show_function_result=True,
        function_result_message="roots: {}",
        default_parameter_group_name="Equation Parameters",
    )

    adapter = GUIAdapter()
    adapter.add(
        equation_solver_4,
        window_config=window_config,
        widget_configs={
            "a": FloatSpinBoxConfig(
                default_value=1.0,
                decimals=5,
                step=0.00005,
            ),
            "b": FloatSpinBoxConfig(decimals=5, step=0.00005),
            "c": FloatSpinBoxConfig(decimals=5, step=0.00005),
        },
    )
    adapter.run()

```

- 使用配置类对象对控件进行配置，首先需要知道参数对应控件的控件配置类是什么，下面的链接展示了`参数数据类型`、`控件类型`、`控件配置对象类型`三者之间的映射关系，开发者若不清楚某个数据类型对应的`控件类型`或`控件配置对象类型`，可以参考该文档：[**控件与参数数据类型**](widget-map.md)。

- 开发者可以阅读以下文档，以获取关于控件属性配置更为详细的说明：[**配置控件属性**](widget-config.md)。

###  3、添加菜单

可以为窗口添加菜单栏，并向菜单栏添加菜单和菜单项，为菜单项设置事件回调。下面，在上述示例代码基础上，演示如何添加菜单并响应事件。

```python
from typing import Optional

from pyguiadapter.action import Action
from pyguiadapter.adapter import GUIAdapter
from pyguiadapter.adapter.uoutput import uprint
from pyguiadapter.exceptions import ParameterError
from pyguiadapter.menu import Menu
from pyguiadapter.utils import messagebox
from pyguiadapter.widgets import FloatSpinBoxConfig
from pyguiadapter.windows.fnexec import FnExecuteWindowConfig, FnExecuteWindow


def equation_solver_5(
    a: float = 1.0, b: float = 0.0, c: float = 0.0
) -> Optional[tuple]:
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
    window_config = FnExecuteWindowConfig(
        title="Equation Solver",
        icon="mdi6.function-variant",
        execute_button_text="Solve",
        size=(350, 450),
        document_dock_visible=False,
        show_function_result=True,
        function_result_message="roots: {}",
        default_parameter_group_name="Equation Parameters",
        # 隐藏`OutputDock`窗口
        output_dock_visible=False,
        # 因为隐藏了`OutputDock`窗口，所以无需将函数调用结果及函数异常信息打印到输出浏览器中
        print_function_error=False,
        print_function_result=False,
    )

    def on_action_about(wind: FnExecuteWindow, action: Action):
        messagebox.show_text_file(
            wind,
            text_file="./about.html",
            text_format="html",
            title="About",
        )

    action_about = Action(text="About", on_triggered=on_action_about)
    menu_help = Menu(title="Help", actions=[action_about])

    adapter = GUIAdapter()
    adapter.add(
        equation_solver_5,
        window_menus=[menu_help],
        window_config=window_config,
        widget_configs={
            "a": FloatSpinBoxConfig(
                default_value=1.0,
                decimals=5,
                step=0.00005,
            ),
            "b": FloatSpinBoxConfig(decimals=5, step=0.00005),
            "c": FloatSpinBoxConfig(decimals=5, step=0.00005),
        },
    )
    adapter.run()

```

**效果如下：**

<div style="text-align: center">
    <img src="/assets/window_menu_demo.gif" />
</div>
**代码说明：**

在上面的代码中，我们添加了一个动作（`Action`）：`action_about`，并为其指定了`triggered`事件响应函数：`on_action_about`，该函数将在动作被触发时调用。

<div style="text-align: center">
 <img src="/assets/l64.png" />
</div>

在`action_about`的事件回调函数中，我们调用`pyguiadapter.utils.messagebox`模块中的`show_text_file()`函数，弹窗展示当前目录下的`about.html`文件：

<div style="text-align: center">
 <img src="/assets/l56.png" />
</div>

然后，创建了一个`Menu`对象：`menu_help`，将其标题设置为"Help"，并将`action_about`添加到其`actions`中：

<div style="text-align: center">
 <img src="/assets/l65.png" />
</div>

最后，将`menu_help`对象添加到`window_menus`中，这样便完成了创建和添加菜单的全过程：

<div style="text-align: center">
 <img src="/assets/l68.png" />
</div>

> - 所谓“动作”（`Action`），就是具有文字、图标等一系列属性，可以响应特定鼠标、快捷键事件的组件。它可以被添加到菜单、工具栏中，当其被添加到菜单中，其表现为菜单项；当其被添加到工具栏时，其表现为工具栏按钮。比如下图中红色方框标记的是同一组`Action`分别在菜单和工具栏中的样子。
>
> <div style="text-align: center">
>  <img src="/assets/actions_demo.png" />
> </div>
>
> - 可以通过鼠标单击或快捷键来“触发”动作。



可以参考以下文档，获取关于窗口菜单栏与工具栏的详细说明：

+ [ 窗口工具栏](toolbar.md)
+ [ 窗口菜单栏 ](menu.md)
