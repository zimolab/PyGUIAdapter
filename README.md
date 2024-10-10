# PyGUIAdapter

## 一、简介

`PyGUIAdapter`是一个用于快速构建图形用户界面的Python库，只需极少的代码，就可以将几乎任意Python函数无缝转化为图形用户界面，大大简化了GUI应用程序的开发过程。`PyGUIAdapter`的核心理念是，以尽可能“无感”和“低侵入性”的方式，帮助开发者建立用户界面，使开发者能够专注于核心功能的实现，而不必将精力分散到复杂、繁琐的GUI编程上，降低了开发者的学习成本和心智负担。



<div style="text-align: center;">
    <img src="docs/images/hello_world.png" />
</div>



## 二、适用场景

`PyGUIAdapter`与“`输入（Input）-处理（Process）-输出（Output）`”程序设计模式高度契合，特别适合用于：

- **工具类应用程序的开发；**
- **将现有的`CLI`应用快速迁移到`GUI`。**

下面是[Python官方文档](https://docs.python.org/3/library/argparse.html#example)给出的一个使用`argparse`创建命令行的例子：

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

借助`PyGUIAdapter`，开发者可以用极少的代码将其转换成GUI程序。

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

<div style="text-align:center">
    <img src="docs/images/process_integers.gif" />
</div>



## 三、特性

* 使用简单，开发快速，可以用极少的代码创建图形用户界面，学习成本低，心智负担小。
* 丰富的内置控件类型，近30种内置控件，基本实现开箱即用。Python的基本数据类型均实现了对应输入控件。同时，对基本类型进行了扩展，提供了丰富的语义类型，方便用户输入日期、时间、颜色、文件路径等特殊对象。实现了通用对象输入控件，支持输入`Json对象`和任意`Python字面量对象`（包括`int`、`float`、`bool`、`str`、`bytes`、`list`、`tuple`、`set`、`dict`）。
* 高度可扩展性，提供了自定义控件接口。开发者可以很方便地为自定义数据类型实现专用输入控件。
* 高度灵活性。控件与窗口均定义了大量可配置属性，开发者可以灵活地调整控件及窗口的外观、样式、行为，提升用户体验。
* 支持使用`QSS`，自由定制界面风格，支持接入现有第三方界面美化库。
* 支持自定义窗口菜单栏、工具栏，支持监听窗口事件，支持动态修改控件，为构建复杂应用提供了可能。
* 基于[`qtpy`](https://github.com/spyder-ide/qtpy)抽象层，不依赖特定Qt绑定库，用户可自由选择`PyQt5`、`PyQt6`、`PySide2`、`PySide2`。
* 界面底层使用`Qt`，兼容性好，相比`webview类`方案，系统资源占用更小。
* 纯Python，跨平台，支持主流桌面操作系统，包括`Windows`、`Linux`、`MacOS`等。


## 四、快速开始

### （一）依赖条件

要使用`PyGUIAdapter`开发应用程序，需满足以下条件：

+ `Python 3.8+`
+ 安装`PyGUIAdapter`
+ 安装Qt的绑定库之一，可选`PyQt5`、`PyQt6`、`PySide2`、`PySide6`

### （二）安装依赖

1、安装`PyGUIAdapter`

```shell
pip install PyGUIAdapter
```

2、安装Qt的绑定库之一，这里以`PySide2`为例：

```shell
pip install pyside2
```

> 如果你的环境下同时安装了多个Qt绑定库，`qtpy`默认会使用`PyQt5`(如果存在的话)。或者可以通过环境变量`QT_API`来明确指定要使用的绑定库，可以指定以下值：
>
> + `pyqt5`
> + `pyside2`
> + `pyqt6`
> + `pyside6`
>
> 更多详细信息，可以参见[qtpy官方说明](https://github.com/spyder-ide/qtpy)。

### （三）编写代码

**1、实现业务逻辑，并封装为函数。**

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

**2、为业务代码适配GUI界面**

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
    <img src="docs/images/equation_solver.gif" />
</div>



## 五、文档

`PyGUIAdapter`还提供了许多高级特性，开发者可以阅读[文档](https://zimolab.github.io/PyGUIAdapter/#/README)，了解`PyGUIAdapter`的高级用法。

## 六、示例代码

为了演示`PyGUIAdapter`的各种功能， 作者编写了大量示例代码，这些代码可以在[example/](https://github.com/zimolab/PyGUIAdapter/tree/main/examples/)目录下找到。

## 七、许可协议

`PyGUIAdapter`使用`MIT`许可协议进行发布。得益于`qtpy`的抽象能力，`PyGUIAdapter`本身并不依赖特定的Qt绑定库。开发者在使用`PyGUIAdapter`开发应用程序时，若依赖特定的Qt绑定库，则在遵守本项目的许可协议的同时，还应当遵守所选绑定库的许可协议。例如：

- 若开发者选择使用`PySide2`，则其须遵守`LGPL`（具体以随附的许可协议为准）。
- 若开发者选择使用`PyQt5`，则其须遵守`GPL`（具体以随附的许可协议为准）。

## 八、致谢

`PyGUIAdapter`依赖如下开源项目，在此向作者表示感谢。

- `qtpy`
- `qtawesome`
- `docstring-parser`
- `tomli`
- `pyqcodeeditor`
- `yapf`

