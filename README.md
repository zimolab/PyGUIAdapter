# PyGUIAdapter

## 一、简介
pyguiadapter是一个基于qtpy的GUI库，它可以简单、快速地为几乎“任意”python函数创建基于PyQt5/PyQt6/PySide2/PySide6的图形用户界面。

借助pyguiadapter，为命令行程序适配图形用户界面的过程将变得无比简单。开发者只需专注于核心功能的实现，将需要对用户提供的功能封装为普通的python
函数，通过参数列表定义用户输入，然后将这个函数传递给pyguiadapter，pyguiadapter将自动为其生成合适的界面，并在背后处理一切有关GUI的细节。

如下图所示，为一个函数创建了一个GUI界面，并恰当地处理用户输入输出，也许仅仅只需要三行代码：

![demo](screenshots/hello_world_demo.png)


## 二、特性
* 使用简单，自动识别函数参数，自动生成输入控件，自动处理用户输入输出。
* 丰富的内置控件类型，涵盖几乎所有常见数据类型，包括：int, float, str, bool, list, dict, tuple, Any, Literal, datetime, date, time等。
同时，从内置类型中扩展了许多语义化类型， 如：file_t, directory_t, color_hex_t等，实现了对应的专属控件，方便用户选择文件、目录、颜色等特定对象。
* 高度的可扩展性，支持为复杂数据类型自定义控件类型。
* 高度的灵活性，窗口、控件提供了大量的可配置属性，可以自定义窗口、控件的外观和行为。
* 支持添加多个函数，提供函数选择界面，支持函数分组。
* 支持函数参数分组。
* 支持窗口菜单和工具栏
* 基于qtpy，用户可以自由选择qt的python绑定库，包括PyQt5/PyQt6/PySide2/PySide6

## 三、安装

1. 安装pyguiadapter库本身

```commandline
pip install pyguiadapter
```

2. 由于pyguiadapter并不依赖特定的Qt库，因此需要先选择一个qt的python绑定库，例如PyQt5、PyQt6、PySide2、PySide6等，以PySide2为例：

```commandline
pip install Pyside2
```

## 四、快速入门

### （一）基本使用

1. 准备一个函数，该函数封装了你要提供给用户的功能，其中需要从用户获取的输入，通过参数列表定义，参数的类型决定了控件的类型，因此需要给参数标志
合适的类型注解，假设我们有一个函数，用于将mp3文件编码为ogg文件，它接受3个参数，一个输入文件路径，一个输出文件路径，一个编码质量参数， 那么可以
这样编写这个函数的签名（这里省略该功能的实现，因为这仅仅是一个演示，我们讨论的是如何使用pyguiadapter）：

```python

def encode_mp3(input_file: str, output_dir: str, output_file: str, quality: int):
    pass
```

2. 导入pyguiadapter库，创建GUIAdapter对象，将函数添加到GUIAdapter对象中，并调用run()方法以启动GUI
```python
from pyguiadapter.adapter import GUIAdapter


if __name__ == '__main__':
    adapter = GUIAdapter()
    adapter.add(encode_mp3)
    adapter.run()
```

3. 运行程序，你将看到一个窗口，通过界面输入参数，点击“Execute”按钮即可调用encode_mp3()函数：

![](screenshots/get_started_1.png)

该示例的完整代码如下，你也可以在此处找到：[get_started.py](examples/get_started_1.py)

```python
from pyguiadapter.adapter import GUIAdapter


def encode_mp3(input_file: str, output_dir: str, output_file: str, quality: int):
    pass


if __name__ == "__main__":
    adapter = GUIAdapter()
    adapter.add(encode_mp3)
    adapter.run()
```

### （二）增强用户体验：PyGUIAdapter的进阶用法

#### 1. 使用语义化的类型

在上面的示例中，参数`input_file`, `output_dir`, `output_file`的类型均被标注为`str`。对于`str`类型的参数，PyGUIAdapter默认会生成一个单行文本输入框，
从本质上讲，这并没有什么根本性的错误，但从语义上看，`input_file`应当代表的是一个文件路径，`output_dir`表示的是一个目录路径，而`output_file`
则代表一个文件名，将这些含义各不相同的统一定义为`str`语义上是不精确的，而且适用于输入通用字符串的单行文本输入框对于输入文件路径、目录路径而言，
并不能为用户带来使用上的便利。考虑到这一点，PyGUIAdapter从一些基本类型扩展出一些更加语义化的类型，并为这些类型实现了更加特定化的控件类型，例如：
针对文件路径，从str扩展了`file_t`，并为其实现文件选择控件；针对目录路径，从str扩展了`directory_t`类型，并实现对应的目录选择控件。一般而言，
使用这些语义化类型，可以大大增强用户体验。

现在，让我们使用这些类型来改善上面的示例：

首先，导入要用的语义化类型，一般而言，这些类型定义在[`pyguiadapter.types`](pyguiadapter/types.py)模块中：

```python
from pyguiadapter.types import file_t, directory_t
```

接着，修改函数签名，使用这些类型标注对应的参数：
```python
def encode_mp3(input_file: file_t, output_dir: directory_t, output_file: str, quality: int):
    pass
```

完整的代码如下，也可以在[这里](examples/get_started_2.py)找到：
```python

from pyguiadapter.adapter import GUIAdapter
from pyguiadapter.types import file_t, directory_t

def encode_mp3(input_file: file_t, output_dir: directory_t, output_file: str, quality: int):
    pass

if __name__ == "__main__":
    adapter = GUIAdapter()
    adapter.add(encode_mp3)
    adapter.run()
```

让我们再次运行程序，看看效果如何：

![](screenshots/get_started_2a.png)

可以看到，参数`input_file`和`output_dir`的控件已经从单行文本输入框变成了文件选择控件（[FileSelect](pyguiadapter/widgets/path/fileselect.py)）
和目录选择控件([DirSelect](pyguiadapter/widgets/path/dirselect.py))。

现在，用户可以通过点击右侧按钮来选择文件和目录，用户体验的提升可以说是立竿见影。

![](screenshots/get_started_2b.png)

#### 扩展：更多语义化类型
除了`file_t`、`directory_t`，PyGUIAdapter还提供了其他语义化类型，可以查看[`pyguiadapter.types`](pyguiadapter/types.py)模块，获取
这些类型的信息。你也可以自行尝试用这些类型对参数进行标注，然后运行程序，观察不同类型所对应的控件有何不同。 

当然，也可以查看[docs/semantic_types.md](docs/semantic_types.md)，其中，对一些常见的语义化类型做了说明。

### 2. 对窗口和控件进行配置

### 3. 参数分组

## 五、自定义控件类型

TODO

## 六、高级主题

TODO

## 七、打包

TODO

## 八、开源许可

得益于qtpy的对不同的qt绑定库以及不同qt版本的抽象，PyGUIAdapter本身并不依赖与特定的qt绑定库，因此其使用MIT开源许可发布。用户利用PyGUIAdapter
开发应用程序，若用到了Qt的python绑定库，则在遵守本项目的许可协议的同时，还必须遵守其所选择的绑定库的许可协议。

例如，若用户选择使用PySide2，则在遵守本项目的许可协议同时，还必须遵守PySide2的许可协议，即LGPL（具体以PySide2随附的许可协议为准）。

又比如，若用户选择使用PyQt5，则在遵守本项目的许可协议同时，还必须遵守PyQt5的许可协议，即GPL（具体以其随附的许可协议为准）。


