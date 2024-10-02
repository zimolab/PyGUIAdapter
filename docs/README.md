# PyGUIAdapter

## 一、概述

`PyGUIAdapter`是一个基于`qtpy`的GUI框架，其核心理念是：以尽可能“低侵入性”和“无感”的方式，帮助Python开发者快速开发图形用户界面程序，使开发者
能够专注于核心功能的实现，而不必将有限的精力分散到用户界面设计和输入输出处理等繁琐、重复、乏味且容易出错的方面。

> 尽管`PyGUIAdapter`基于`qtpy`，但一般而言，使用`PyGUIAdapter`并不要求开发者掌握`qtpy`或`Qt`相关知识。当然，在涉及自定义控件等高级主题时，
> 情况有所不同，此时需要开发者对`qtpy`（或者`PyQt5/6`、`PySide2/6`等绑定库）有一定了解。

`PyGUIAdapter`使图形用户界面程序的开发变得轻松写意，甚至允许开发者在不编写一行GUI代码（或CLI代码）的情况下，构建简洁高效的图形用户界面，大大降低了
开发者的学习成本和心智负担。

![hello_world](images/hello_world.png)

借助`PyGUIAdapter`，从`CLI`切换到`GUI`将变得十分简单和平滑。

下面是Python[官方文档](https://docs.python.org/3/library/argparse.html#example)给出的一个使用`argparse`创建命令行程序的例子：

```python
import argparse
parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('integers', metavar='N', type=int, nargs='+',
                    help='an integer for the accumulator')
parser.add_argument('--sum', dest='accumulate', action='store_const',
                    const=sum, default=max,
                    help='sum the integers (default: find the max)')

args = parser.parse_args()
print(args.accumulate(args.integers))
```

在`PyGUIAdapter`帮助下，开发者可以从此告别编写冗长、乏味的`argument/option`代码，而将全部精力集中到核心功能的实现上：

```python
from typing import List, Literal
from pyguiadapter.adapter import GUIAdapter


def process_integers(
    integers: List[int], operation: Literal["sum", "max"] = "max"
) -> int:
    """
    Process some integers.

    @param integers: an integer for the accumulator
    @param operation: sum the integers (default: find the max)
    """
    func = max if operation == "max" else sum
    return func(integers)


if __name__ == "__main__":
    adapter = GUIAdapter()
    adapter.add(process_integers)
    adapter.run()

```

![process_integers.png](images/process_integers.png)


## 二、特性

* 使用简单，开发快速，可以用极少的代码创建图形用户界面，学习成本低，心智负担小。
* 丰富的内置控件类型，近30种内置控件，基本实现开箱即用。Python的基本数据类型均实现了对应输入控件。同时，对基本类型进行了扩展，提供了丰富的语义类型，方便用户输入日期、时间、颜色、文件路径等特殊数据对象。实现了通用对象输入控件，支持输入Json对象和任意Python字面量对象（包括`int`、`float`、`bool`、`str`、`bytes`、`list`、`tuple`、`set`、`dict`）。
* 高度可扩展性，提供了自定义控件接口。开发者可以很方便地为自定义数据类型实现专用输入控件。
* 高度的灵活性。提供了大量可配置属性，开发者可以灵活地调整窗口及控件的外观、样式、行为，提升用户体验。支持使用QSS对界面进行美化，支持接入第三方界面美化库。
* 支持自定义窗口菜单栏、工具栏，支持监听窗口事件，支持动态修改参数控件，为构建复杂应用提供了可能。
* 基于[`qtpy`](https://github.com/spyder-ide/qtpy)抽象层，不依赖特定Qt的Python绑定库，用户可自由选择`PyQt5`、`PyQt6`、`PySide2`、`PySide2`。
* 界面底层使用`Qt`，兼容性好，对高分屏的支持更加友好，相比webview类方案，性能更好，内存占用更低。
* 跨平台，支持主流桌面操作系统，包括Windows、Linux、MacOS等。


## 三、开始入门

### （一）依赖条件

使用`PyGUIAdapter`开发应用程序，需要满足以下条件：
+ Python 3.8+
+ 安装`PyGUIAdapter`
+ 安装Qt的绑定库之一，可选`PyQt5`、`PyQt6`、`PySide2`、`PySide6`

> `PyGUIAdapter`本身依赖如下项目：
> + `qtpy`
> + `qtawesome`
> + `docstring-parser`
> + `tomli`
> + `pyqcodeeditor`

### （二）安装依赖

1、安装`PyGUIAdapter`本身

```shell
pip install PyGUIAdapter
```

2、安装Qt的绑定库之一，这里以`PySide2`为例：

```shell
pip install pyside2
```

> 如果你的环境下同时安装了多个Qt的绑定库，qtpy默认会使用`PyQt5`(如果存在的话)。或者你可以通过环境变量`QT_API`来明确指定要使用的绑定库，可以指定以下值：
>
> + pyqt5
> + pyside2
> + pyqt6
> + pyside6
>
> 更多详细信息，可以参见：[qtpy官方说明](https://github.com/spyder-ide/qtpy)。

### （三）一个简单的示例

`PyGUIAdapter`以函数为基本单元。在开发时，开发者的主要工作是实现业务逻辑并将其封装为Python函数。在这一过程中，开发者将希望用户输入数据以函数参数的形式列在参数列表中，并使用[`类型注解`](https://peps.python.org/pep-0484/)正确标注其数据类型。剩下的工作，基本上就可以交由`PyGUIAdapter`自动完成了:

在运行时，`PyGUIAdapter`会提取函数的参数列表，并根据每一个参数的类型，自动选择合适的控件，例如：对于`int`类型的参数，`PyGUIAdapter`将默认创建
一个`IntSpinBox`；对于`str`类型的参数，`PyGUIAdapter`将默认创建一个`LineEdit`等等。除此之外，`PyGUIAdapter`还将自动完成窗口创建、界面布局
和事件绑定等工作。在用户点击`Execute`按钮时，`PyGUIAdapter`将自动调用目标函数，在此之前，`PyGUIAdapter`自动从界面中收集用户输入的数据，并将
这些数据作为参数传递给目标函数。

> `PyGUIAdapter`充分利用了Python的类型注解机制。在`PyGUIAdapter`中，函数参数的类型注解不是那种可有可无的东西，它是生成参数控件的决定性因素。
> 虽然并不是说不使用类型注解就完全无法利用`PyGUIAdapter`——`PyGUIAdapter`也允许开发者手动为每一个参数显式地指定控件的类型——但是，那样会在很大程度
> 上失去使用`PyGUIAdapter`的意义。所以，**我们强烈建议开发者养成在函数参数上使用类型注解的开发习惯**，如果能够做到这一点的，那么我相信，未来
> 一定会很多人会感激你，甚至包括你自己。

#### 1、基本代码结构

下面通过一个简单的实例来说明`PyGUIAdapter`的基本使用方法。 假设，现在要求我们实现一个简单的`一元二次方程求解器`。

根据定义，要确定一个`一元二次方程`，需要知道三个系数：`a`、`b`、`c`。由此，可以确定求解函数应当有三个输入参数：`a`、`b`、`c`。又因为方程系数一般为实数（为了演示的简单性，这里不考虑复数的情况），由此可以确定这三个参数的类型应当为`float`。 下面，我们根据这些信息，使用求根公式来实现求解函数`solve()`：

```python
import math

def solve(a: float, b: float, c: float) -> list:
    """
    Equation Solver, solving equations like:

    **ax^2 + bx + c = 0** (a,b,c ∈ R)
    """
    discriminant = b**2 - 4 * a * c
    if discriminant < 0:
        return []
    elif discriminant == 0:
        return [-b / (2 * a)]
    else:
        sqrt_discriminant = math.sqrt(discriminant)
        return [(-b + sqrt_discriminant) / (2 * a), (-b - sqrt_discriminant) / (2 * a)]
```

接着，我们为`solve()`函数适配图形界面，对于这个简单的例子，基本上只需要三行代码而无需其他额外的工作，即可完成图形界面的适配：

```python
adapter = GUIAdapter()
adapter.add(solve)
adapter.run()
```

完整代码如下：

```python
import math
from pyguiadapter.adapter import GUIAdapter


def solve(a: float, b: float, c: float) -> list:
    """
    Equation Solver, solving equations like:

    **ax^2 + bx + c = 0** (a,b,c ∈ R)
    """
    discriminant = b**2 - 4 * a * c
    if discriminant < 0:
        return []
    elif discriminant == 0:
        return [-b / (2 * a)]
    else:
        sqrt_discriminant = math.sqrt(discriminant)
        return [(-b + sqrt_discriminant) / (2 * a), (-b - sqrt_discriminant) / (2 * a)]


if __name__ == "__main__":
    adapter = GUIAdapter()
    adapter.add(solve)
    adapter.run()
```



<img src="images/solver.png" />

>如上图所示，`PyGUIAdapter`生成的窗口主要包含三个区域：
>
>1. **参数控件区（Parameters Area）**：从函数参数生成的输入控件将放置在此区域
>
>2. **函数文档停靠窗口（Document Dock）**：该区域主要用于显示函数的文档信息，其显示的内容默认来源于函数的`文档字符串（docstring）`
>
>3. **程序输出停靠窗口（Output Dock）**：该区域主要用于显示程序的输出信息，函数的返回值、函数调用过程中发生的异常信息默认将显示在此区域。

下面，尝试输入`a`为零，这将使函数发生除以0的异常，看看`PyGUIAdapter`如何处理函数中`未捕获的异常`：

<img src="images/error_handling.png" width="60%"/>

对于函数中的异常，`PyGUIAdapter`的默认策略是：***捕获它们，弹窗提醒用户，并在程序输出区域打印其堆栈信息。** 这样的设计主要是为了增强程序的`健壮性`，
防止未捕获的异常导致整个程序崩溃。

#### 2、在函数中打印信息

> 关于这一主题，以下文档作了更为详细的说明：[向窗口输出信息](adapter/output.md)

在程序运行过程中向用户打印一些信息是一个常见需求，一般使用内置函数`print()`来打印信息。然而，通过`print()`打印的信息通常会被输出到`stdout`（一般而言就是控制台），因此用户无法在`程序输出停靠窗口`中看到这些信息。为了使开发者能够将信息打印到`程序输出停靠窗口`中，`PyGUIAdapter`提供了`uprint()`函数，其用法与`print()`基本一致，下面演示如何使用该方法：

> Tips：从`pyguiadapter.adapter.uoutput`模块导入`uprint()`函数

```python
import math
from pyguiadapter.adapter import GUIAdapter
from pyguiadapter.adapter.uoutput import uprint


def solve(a: float, b: float, c: float) -> list:
    """
    Equation Solver, solving equations like:

    **ax^2 + bx + c = 0** (a,b,c ∈ R)
    """
    uprint("Solving Equation:")
    uprint(f"  {a}x² + {b}x + {c} = 0")
    discriminant = b**2 - 4 * a * c
    uprint(f"  Δ = {discriminant}", end="")
    if discriminant < 0:
        uprint(" < 0, no real roots")
        return []
    elif discriminant == 0:
        uprint(" = 0, one real root")
        return [-b / (2 * a)]
    else:
        uprint(" > 0, two real roots")
        sqrt_discriminant = math.sqrt(discriminant)
        return [(-b + sqrt_discriminant) / (2 * a), (-b - sqrt_discriminant) / (2 * a)]


if __name__ == "__main__":
    adapter = GUIAdapter()
    adapter.add(solve)
    adapter.run()

```
<img src="images/uprint.png" width="60%"/>

> `uprint()`函数支持输出html格式内容，但只支持部分标签。

除了`uprint()`函数，`pyguiadapter.adapter.uoutput`模块中还有许多输出信息的方法，借助这些方法，开发者可以输出格式更加丰富的的信息。

```python
from pyguiadapter.adapter import GUIAdapter, uoutput

def output_log_msg(
    info_msg: str = "info message",
    debug_msg: str = "debug message",
    warning_msg: str = "warning message",
    critical_msg: str = "critical message",
    fatal_msg: str = "fatal message",
):
    uoutput.info(info_msg)
    uoutput.debug(debug_msg)
    uoutput.warning(warning_msg)
    uoutput.critical(critical_msg)
    uoutput.fatal(fatal_msg)


if __name__ == "__main__":
    adapter = GUIAdapter()
    adapter.add(output_log_msg)
    adapter.run()

```

<img src="images/ulogging.png" width="60%"/>

由于`uprint()`支持输出`html`格式的信息，因此开发者甚至可以将图片输出到`Output`窗口中：

> `uprint()`对`html`的支持有限，仅支持部分html标签，不支持`css3`和`html5`。

#### 3、对函数参数进行校验

虽然`PyGUIAdapter`对程序中的未捕获异常进行了处理，但我们仍然鼓励开发者尽力预见并避免可能发生的异常，因为这是提高程序健壮性、稳定性的基础之一。
而程序中的异常或错误，很多时候源自于未经检验的用户输入，基于**“永远不要相信用户的输入”**这一共识，开发者都应当对函数参数进行必要的校验。

对于函数参数的合法性校验，`PyGUIAdapter`提供了一种特殊但非常简单、直接的机制，不同于其他库中的做法，`PyGUIAdapter`不要求开发者为每个参数提供类似于`Validator`
的东西。开发者仍然需要在函数中手动编写参数校验代码，只不过，对于非法的参数，开发者可以抛出`ParameterError`，`PyGUIAdapter`在捕获到此类特殊异常时，
会做出一些特殊的处理：

```python
import math
from pyguiadapter.adapter import GUIAdapter
from pyguiadapter.adapter.uoutput import uprint
from pyguiadapter.exceptions import ParameterError


def solve(a: float, b: float, c: float) -> list:
    """
    Equation Solver, solving equations like:

    **ax^2 + bx + c = 0** (a,b,c ∈ R)
    """

    if a == 0:
        raise ParameterError(parameter_name="a", message="a cannot be zero")

    uprint("Solving Equation:")
    uprint(f"  {a}x² + {b}x + {c} = 0")
    discriminant = b**2 - 4 * a * c
    uprint(f"  Δ = {discriminant}", end="")
    if discriminant < 0:
        uprint(" < 0, no real roots")
        return []
    elif discriminant == 0:
        uprint(" = 0, one real root")
        return [-b / (2 * a)]
    else:
        uprint(" > 0, two real roots")
        sqrt_discriminant = math.sqrt(discriminant)
        return [(-b + sqrt_discriminant) / (2 * a), (-b - sqrt_discriminant) / (2 * a)]


if __name__ == "__main__":
    adapter = GUIAdapter()
    adapter.add(solve)
    adapter.run()

```
<img src="images/parameter_error.png" width="60%"/>

可以看到，**对于函数中抛出的`ParameterError`，`PyGUIAdapter`不仅进行了弹窗提示，而且在对应参数的输入控件下方，以醒目的方式提醒用户他刚刚输入
了一个不合法的值。**

## 四、高级主题

### （一）数据类型与控件

#### 1、[配置函数参数控件的类型与属性](widgets/configure_widget)

#### 2、[内置控件类型一览](widgets/types_and_widgets.md)

#### 3、[创建和使用自定义控件](widgets/custom_widget.md)

#### 4、[关于图标](widgets/icons.md)

### （二）`pyguiadapter.adapter.*`

#### 1、[添加多个函数：函数名称、图标、文档及分组](adapter/multiple_functions.md)

#### 2、[用户进行交互：消息对话框与输入对话框](adapter/interact.md)

#### 3、[取消正在执行的函数：协商式线程退出机制](adapter/cancellable_function.md)

#### 4、[使用进度条](adapter/progressbar.md)

#### 5、[界面美化：使用样式表与第三方库](adapter/style.md)


### （三）窗口

在`PyGUIAdapter`中，主要有两类窗口，分别是`函数选择窗口（FnSelectWindow）`和`函数执行窗口（FnExecutWindow）`。

1. `函数选择窗口`：该窗口用于选择要执行的函数，当开发者向`GUIAdapter`实例中添加了超过一个函数时，会自动显示该窗口。开发者也可以在强制显示该窗口（即使实例中只添加了一个函数），方法是在调用`GUIAdapter.run()`时传入`show_select_window=True`。
2. `函数执行窗口`：该窗口用于接受函数的参数，并执行函数。

上述两类窗口均提供了大量的配置选项，开发者可以根据需要自由调整这些配置选项，以实现更加定制化的界面。下面是窗口相关的一些高级用法。

#### 1、[窗口概述](windows/overview.md)

#### 2、[为窗口添加工具栏](windows/toolbar.md)

#### 3、[为窗口添加菜单栏](windows/menus.md)

#### 4、[监听窗口事件](windows/window_event.md)

#### 5、[函数选择窗口（FnSelectWindow）](windows/fn_select_window.md)

#### 6、[函数执行窗口（FnExecuteWindow）](windows/fn_exec_window.md)

### （四）实用工具

> TODO

### （五）打包应用

> TODO


## 五、教程

上面的示例代码演示了`PyGUIAdapter`的基本用法。 除此之外，`PyGUIAdapter`为构建更加大型、复杂的应用程序，提供了更多的功能。

下面是一些案例教程，通过逐步构建一个完整的应用程序，开发者可以学到`PyGUIAdapter`的进阶用法。

> TODO



## 六、开源协议

得益于`qtpy`的抽象能力，`PyGUIAdapter`本身并不依赖特定的qt绑定库，因此`PyGUIAdapter`使用`MIT`许可协议。
开发者在使用`PyGUIAdapter`开发应用程序时，若依赖特定的Qt绑定库，则其在遵守本项目的许可协议的同时，还必须遵守其所选择的绑定库的许可协议。

例如：
- 若开发者选择使用`PySide2`，则其必须遵守`LGPL`（具体以其随附的许可协议为准）。
- 若开发者选择使用`PyQt5`，则其必须遵守`GPL`（具体以其随附的许可协议为准）。


## 七、贡献

参见：[CONTRIBUTING.md](CONTRIBUTING.md)