# PyGUIAdapter

## 一、概述

`PyGUIAdapter`是一个基于`qtpy`的GUI框架，其核心理念是：以尽可能“低侵入性”和“无感”的方式，帮助Python开发者快速开发图形用户界面程序，使开发者能够专注于核心功能的实现，而不必将有限的精力分散到用户界面设计和输入输出处理等繁琐、重复、乏味且容易出错的方面。

> 尽管`PyGUIAdapter`基于`qtpy`，但一般而言，使用`PyGUIAdapter`并不要求开发者掌握`qtpy`或`Qt`相关知识。当然，在涉及自定义控件等高级主题时，情况有所不同，此时需要开发者对`qtpy`（或者`PyQt5/6`、`PySide2/6`等绑定库）有一定了解。

`PyGUIAdapter`使图形用户界面程序的开发变得轻松写意，甚至允许开发者在不编写一行GUI代码（或CLI代码）的情况下，构建简洁高效的图形用户界面，大大降低了开发者的学习成本和心智负担。

![hello_world](/images/hello_world.png)

借助`PyGUIAdapter`，从`CLI程序`切换到`GUI程序`将变得十分顺滑。

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

上面的示例代码来自Python[官方文档](https://docs.python.org/3/library/argparse.html#example)。在`PyGUIAdapter`帮助下，开发者可以从此告别编写冗长、乏味的`argument/option`代码，而将全部精力投注到核心功能的实现上。

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

![process_integers.png](/images/process_integers.png)


## 二、特性

* 使用简单，开发快速，可以用极少的代码创建图形用户界面，学习成本低，心智负担小。
* 丰富的内置控件类型，可以实现开箱即用。为python基本数据类型实现了对应输入控件。同时，对基本类型进行了扩展，提供了丰富的语义类型，使用用户在输入日期、时间、颜色、文件路径等特殊对象时，能够更加方便、精准。
* 高度的可扩展性，提供了自定义控件接口。开发者可以很方便地为复杂的自定义数据类型，实现特定的输入控件。
* 高度的灵活性。提供了大量可配置属性，开发者可以灵活地调整界面的外观、样式，或者是更加精细地控制控件的行为，提升用户体验。
* 支持自定义窗口菜单栏、工具栏，为构建复杂应用提供了可能。
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

> 如果你的环境下同时安装了多个Qt的绑定库，qtpy默认会使用`PyQt5`(如果存在的话)。
> 或者你可以通过环境变量`QT_API`来明确指定要使用的绑定库，可以指定以下值：
> + pyqt5
> + pyside2
> + pyqt6
> + pyside6
>
> 更多详细的说明，参见：[qtpy官方说明](https://github.com/spyder-ide/qtpy)。

### （三）基本用法

`PyGUIAdapter`以函数为基本单元。在开发时，开发者的主要工作是实现业务逻辑并将其封装为Python函数。在这一过程中，开发者将希望用户输入数据以函数参数的形式列在参数列表中，并使用[`类型注解`](https://peps.python.org/pep-0484/)正确标注其数据类型。剩下的工作，基本上就可以交由`PyGUIAdapter`自动完成了:

在运行时，`PyGUIAdapter`会提取函数的参数列表，并根据每一个参数的类型，自动选择合适的控件，例如：对于`int`类型的参数，`PyGUIAdapter`将默认创建一个`IntSpinBox`；对于`str`类型的参数，`PyGUIAdapter`将默认创建一个`LineEdit`等等。除此之外，`PyGUIAdapter`还将自动完成窗口创建、界面布局和事件绑定等工作。在用户点击`Execute`按钮时，`PyGUIAdapter`将自动调用目标函数，在此之前，`PyGUIAdapter`自动从界面中收集用户输入的数据，并将这些数据作为参数传递给目标函数。

#### 1、 一个简单的示例

> 下面实现一个简单的`一元二次方程求解器`

##### （1）基本用法

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

如上图所示，`PyGUIAdapter`自动生成的窗口主要包含三个区域：

1. **参数控件区（Parameters Area）**：从函数参数生成的输入控件将放置在此区域

2. **函数文档停靠窗口（Document Dock）**：此区域主要用于显示函数的文档信息，其显示的内容默认来源于函数的`文档字符串（docstring）`

3. **程序输出停靠窗口（Output Dock）**：此区域主要用于显示程序的输出信息，函数的返回值、函数调用过程中发生的异常信息默认将显示在此区域。

下面，让我们将参数`a`调整为零，尝试使函数发生异常，**看看`PyGUIAdapter`如何处理函数中`未捕获的异常`**：

<img src="images/error_handling.png" width="60%"/>

对于函数中的异常，`PyGUIAdapter`的默认策略是：***捕获它们，弹窗提醒用户，并在程序输出区域打印其堆栈信息。** 这样的设计主要是为了增强程序的`健壮性`，防止未捕获的异常导致整个程序崩溃。

##### （2）输出信息

在程序运行过程中向用户打印一些信息是一个非常常见的需求，一般我们使用内置函数`print()`来做到这一点。然而，通过`print()`打印的信息通常会被输出到`stdout`，因此用户无法在`程序输出停靠窗口`中看到这些信息。为了使开发者能够将信息打印到`程序输出停靠窗口`中，`PyGUIAdapter`提供了`uprint()`函数，其用法与`print()`基本一致，下面演示如何使用该方法：

> Tips：从`pyguiadapter.adapter.ulogging`模块导入`uprint()`函数

```python
import math
from pyguiadapter.adapter import GUIAdapter
from pyguiadapter.adapter.ulogging import uprint


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


除了`uprint()`函数，`pyguiadapter.adapter.ulogging`模块还有许多输出信息的方法，借助这些方法，开发者可以输出格式更加丰富的的信息。

```python
from pyguiadapter.adapter import GUIAdapter, ulogging

def output_log_msg(
    info_msg: str = "info message",
    debug_msg: str = "debug message",
    warning_msg: str = "warning message",
    critical_msg: str = "critical message",
    fatal_msg: str = "fatal message",
):
    ulogging.info(info_msg)
    ulogging.debug(debug_msg)
    ulogging.warning(warning_msg)
    ulogging.critical(critical_msg)
    ulogging.fatal(fatal_msg)


if __name__ == "__main__":
    adapter = GUIAdapter()
    adapter.add(output_log_msg)
    adapter.run()

```

<img src="images/ulogging.png" width="60%"/>


##### （3）校验参数

虽然`PyGUIAdapter`对程序中的未捕获异常进行了处理，但我们仍然鼓励开发者尽力预见并避免可能发生的异常，因为这是提高程序健壮性、稳定性的基础之一。
而程序中的异常或错误，很多时候源自于未经检验的用户输入，基于**“永远不要相信用户的输入”**这一共识，开发者都应当对函数参数进行必要的校验。

对于函数参数的合法性校验，`PyGUIAdapter`提供了一种特殊但非常简单、直接的机制，不同于其他库中的做法，`PyGUIAdapter`不要求开发者为每个参数提供类似于`Validator`
的东西。开发者仍然需要在函数中手动编写参数校验代码，只不过，对于非法的参数，开发者可以抛出`ParameterError`，`PyGUIAdapter`在捕获到此类特殊异常时，
会做出一些特殊的处理：

```python
import math
from pyguiadapter.adapter import GUIAdapter
from pyguiadapter.adapter.ulogging import uprint
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

可以看到，**对于函数中抛出的`ParameterError`，`PyGUIAdapter`不仅进行了弹窗提示，而且在对应参数的输入控件下方，以醒目的方式提醒用户他刚刚输入了一个不合法的值。**

#### 2、一个更加复杂的示例


## 四、进阶用法

## 五、开源许可

## 六、贡献

## 七、其他说明

## 八、版本更新