## （一）前言

为了便于分发和部署，可以将开发好的应用打包成二进制可执行文件，这样用户可以在不安装Python解释器和相关程序库的环境下运行程序。笔者测试了`pyinstaller`打包工具，发现其可以应用进行打包，下面以一个具体的Demo项目为例，对使用`pyinstaller`打包进行讲解。本文中涉及的所有代码、资源文件、打包配置文件等均可以在以下目录中找到：

- [examples/packaging/]({{main_branch}}/examples/packaging/)

此外，强烈建议开发者在python虚拟环境中对应用进行打包，这样可以避免将许多未用到的库和文件打包到最终的产物中，从而减少可执行文件的体积。



## （二）准备工作

首先，需要安装`pyinstaller`打包工具：

### 1、使用pip

```bas
pip install pyinstaller
```

### 2、使用poetry

```bash
poetry add pyinstaller --group dev
```

安装过程中，可能会因为`python`版本问题，导致安装失败。提示信息大概如下：

```
The current project's supported Python range (>=3.8,<4.0) is not compatible with some of the required packages Python requirement:
  - pyinstaller requires Python <3.14,>=3.8, so it will not be satisfied for Python >=3.14,<4.0

Because no versions of pyinstaller match >6.10.0,<7.0.0
 and pyinstaller (6.10.0) requires Python <3.14,>=3.8, pyinstaller is forbidden.
So, because pyguiadapter depends on pyinstaller (^6.10.0), version solving failed.

  • Check your dependencies Python requirement: The Python requirement can be specified via the `python` or `markers` properties

    For pyinstaller, a possible solution would be to set the `python` property to ">=3.8,<3.14"

    https://python-poetry.org/docs/dependency-specification/#python-restricted-dependencies,
    https://python-poetry.org/docs/dependency-specification/#using-environment-markers
    https://python-poetry.org/docs/dependency-specification/#using-environment-markers   
```

此时，需要将`pyproject.toml`文件中`python`依赖项的版本设置到正确的范围，比如：

```toml
...
[tool.poetry.dependencies]
python = "^3.8, <3.14"
...
```

然后再次运行`poetry add pyinstaller --group dev`。

## （三）开始打包

首先需要进入[examples/packaging/]({{main_branch}}/examples/packaging/)目录，以下命令行均在此目录下完成。

```shell
cd example/packaging/
```

### 1、基础命令

`pyinstaller`的命令语法如下：

```bash
pyinstaller [options] script [script …] | specfile
```

首先，让我们尝试不加任何选项来打包我们的应用，在命令行下输入：

```bash
pyinstaller app.py
```

不出意外，我们将看到类似下面的输出：

```
...
20490 INFO: Fixing EXE headers
20566 INFO: Building EXE from EXE-00.toc completed successfully.
20569 INFO: checking COLLECT
20571 INFO: Building COLLECT COLLECT-00.toc
20786 INFO: Building COLLECT COLLECT-00.toc completed successfully.
```

这表明打包已经成功了，此时，`examples/packaging/`目录下会出现两个新的目录`build`和`dist`，以及一个新的文件`app.spec`：

- `build/`：该目录用于存放打包过程中生成的一些中间文件，一般无需过多关注。
- `dist/`：该目录用于存放打包的结果产物，我们需要的二进制可执行文件就将被放到这个命令下
- `app.spec`：`*.spec`文件时打包配置文件，该文件记录了打包所使用的参数，运行打包命令后将自动生成该文件。后续可以直接输入`pyinstaller app.spec`命令打包应用，而无需每次都手动输入参数。

<div style="text-align: center;">
    <img src="/assets/packaging_1.png" />
</div>


现在让我们查看`dist`目录，里面包含一个名为`app`的子目录，最终的可执行文件就在该目录下。默认情况下，`pyinstaller`会生成一个可执行文件及一个`_internal/`目录：

<div style="text-align: center;">
    <img src="/assets/packaging_2.png" />
</div>

`_internal/`目录下存放着这可执行文件运行时依赖的库和其他文件：

<div style="text-align:center">
    <img src="/assets/packaging_3.png" />
</div>

### 2、打包资源（数据）文件

#### （1）第三方依赖中的资源文件

现在，让我们运行`app.exe`，结果发现只有一个命令行窗口一闪而过，程序没有启动成功。这说明打包还存在一些问题，并没有真正成功。让我们通过命令行再次启动`app.exe`，尝试从其命令行输出中定位问题所在。

```python
./dist/app/app.exe
```

程序输出了大段的异常回溯信息，让我们截取其中关键的部分：

```
Traceback (most recent call last):
  ...
  File "yapf_third_party\_ylib2to3\pygram.py", line 29, in <module>
  File "yapf_third_party\_ylib2to3\pgen2\driver.py", line 237, in load_grammar
  File "pkgutil.py", line 637, in get_data
  File "PyInstaller\loader\pyimod02_importers.py", line 509, in get_data
FileNotFoundError: [Errno 2] No such file or directory: '...\\dist\\app\\_internal\\yapf_third_party\\_ylib2to3\\Grammar.txt'
```

从异常信息中不难发现，一些程序运行所必须的文件没有被打包到`_internal/`目录下，具体而言，该文件被第三方包`yapf_third_party`引用。

`PyGUIAdapter`依赖`yapf`实现代码格式化功能，而`yapf`在内部依赖又了`yapf_third_party`。显然，目前`pyinstaller`还无法处理`yapf`这种依赖关系，无法自动收集并打包其所需的文件。为了处理类似的错误，我们可以手动指定需要收集的文件的包或模块，`pyinstanller`提供了以下选项：

- `--hidden-import MODULENAME`或 `--hiddenimport MODULENAME`[](https://pyinstaller.org/en/stable/usage.html#cmdoption-hidden-import)

  用于告诉`pyInstaller`在打包过程中包含那些可能没有被自动识别为依赖的额外python包，即那些通过`importlib`等方式隐式导入的包。

- `--collect-submodules MODULENAME`[](https://pyinstaller.org/en/stable/usage.html#cmdoption-collect-submodules)

  用于收集指定包或模块的所有子模块。

- `--collect-data MODULENAME`或`--collect-datas MODULENAME`[](https://pyinstaller.org/en/stable/usage.html#cmdoption-collect-data)

  用于收集指定包或模块下的数据文件。

- `--collect-binaries MODULENAME`[](https://pyinstaller.org/en/stable/usage.html#cmdoption-collect-binaries)

  用于收集指定包或模块下的二进制文件。

- `--collect-all MODULENAME`[](https://pyinstaller.org/en/stable/usage.html#cmdoption-collect-all)

  用于指定包或模块下的所有子模块、数据文件、二进制文件。

现在，让我们手动指定需要收集资源文件的第三方依赖。除了`yapf_third_party`，还有`pyqcodeeditor`。

> [`pyqcodeeditor`]()是作者移植的一个代码编辑器控件，`PyGUIAdapter`使用了该控件。`pyqcodeeditor`内置了一些用于定义语法和高亮规则的`json`文件，`pyinstaller`还没办法自动收集这些文件，因此也需要手动收集这些文件。

```shell
 pyinstaller app.py --collect-data yapf_third_party --collect-data pyqcodeeditor -y --clean
```

这里使用了两个新的选项`-y`和`--clean`。其含义和用途如下：

- `-y`

指定该选项后，如果存在之前生成的文件，直接进行覆盖，不会询问是否要移除它们。

- `--clean`

清除缓存，并移除之前构建时产生的临时文件。



打包完成后。可以发现，`yapf_third_party`和`pyqcodeeditor`中的资源文件打包到`_internal`目录下了。

<div style="text-align:center">
    <img src="/assets/packaging_4.png" />
</div>

让我们再次运行`app.exe`，已经可以正常显示程序界面了。

<div style="text-align:center">
    <img src="/assets/packaging_5.gif" />
</div>
**小结：**如果程序引用了一些第三方库，而`pyinstaller`目前还无法自动收集这些库或是其资源文件，开发者可以使用`--collect-xxx`选项手动包含需要的文件。

#### （1）项目资源文件

现在，我们的应用仍然存在一个小问题：当我们单击`Help`菜单下的`About`菜单项，本应弹出一个关于对话框，但是，什么都没有发生。

<div style="text-align:center">
    <img src="/assets/packaging_6.gif" />
</div>

让我们从命令行输出中定位问题：

```
Traceback (most recent call last):
  File "pyguiadapter\window.py", line 361, in _on_triggered
  File "app.py", line 40, in on_action_about
  File "pyguiadapter\utils\messagebox.py", line 264, in show_text_file
  File "pyguiadapter\utils\io.py", line 2, in read_text_file
FileNotFoundError: [Errno 2] No such file or directory: '...\\dist\\app\\_internal\\about.html'
```

非常清晰的错误消息：`app.py`的第`40行`用到了一个文件`about.html`，但该文件并不存在。

<div style="text-align:center">
    <img src="/assets/packaging_7.png" />
</div>

`about.html`与`app.py`在同一目录下，`pyinstaller`在打包时却没有将`about.html`打包到`_internal`目录下，这就是问题的根源。因此，我们需要手动指定项目中哪些资源文件需要被打包到最终产物中。对此，`pyinstaller`提供了`--add-data`选项。

> `--add-data SOURCE:DEST`[](https://pyinstaller.org/en/stable/usage.html#cmdoption-add-data)
>
> Additional data files or directories containing data files to be added to the application. The argument value should be in form of “source:dest_dir”, where source is the path to file (or directory) to be collected, dest_dir is the destination directory relative to the top-level application directory, and both paths are separated by a colon (:). To put a file in the top-level application directory, use . as a dest_dir. This option can be used multiple times.

让我们添加需要打包的文件，然后再次进行打包：

```bash
pyinstaller app.py  --collect-data yapf_third_party --collect-data pyqcodeeditor --add-data "./about.html:./" -y --clean
```

> `--add-data "./about.html:./"`的含义是：把`当前目录（./）`下的`about.html`文件打包到`目标产物的根目录(./)`下
>
> 而在新版本的`pyinstaller`中，最终产物的根目录就是`_internal`目录。

打包完成后，可以发现`about.html`已经被打包到`_internal`目录下了。

<div style="text-align:center">
    <img src="/assets/packaging_8.png" />
</div>

再次运行`app.exe`，现在终于可以正常弹出对话框了：

<div style="text-align:center">
    <img src="/assets/packaging_9.gif" />
</div>

#### （3）关于文件路径的一些提示

为了在程序打包后仍然可以访问到项目中的资源文件，需要在代码中必须非常小心的除了路径问题，尤其是采用`相对路径`时，源码状态下和打包状态下`相对路径`中**“相对”**的含义是不同的，具体而言，**“相对”的起点**不同。为了解决这个问题，一种可行的方法是，以`__file__`为起点对路径进行定位，本例中就是采用这种做法。

<div style="text-align:center">
    <img src="/assets/packaging_10.png" />
</div>

## （四）修改可执行文件名称、图标

### 1、修改可执行文件名

默认情况下，`pyinstaller`生成的二进制文件名称将与输入的源码文件名称一致。比如，在`windows`平台下，`app.py`打包后的二进制可执行文件名默认为`app.exe`。当然，`pyinstaller`允许我们指定可执行文件的名称，方法是使用`--name`选项。

>`-n NAME`, `--name NAME`[](https://pyinstaller.org/en/stable/usage.html#cmdoption-n)
>
>Name to assign to the bundled app and spec file (default: first script’s basename)

现在，让我们把程序名称修改为`Equation-Solver`。

首先，把之前生成的`dist`、`build`、`app.spec`文件删除。然后运行以下命令：

```bash
pyinstaller app.py --name "Equation-Solver"  --collect-data yapf_third_party --collect-data pyqcodeeditor --add-data "./about.html:./" -y --clean
```

打包完成后，重新生成了一个`.spec`文件，名称为`Equation-Solver.spec`。在`dist/Equation-Solver`目录下，生成了一个名为`Equation-Solver.exe`的可执行文件。

<div style="text-align:center">
    <img src="/assets/packaging_11.png" />
</div>

### 2、修改可执行文件的图标

`pyinstaller`生成的可执行文件具有一个默认的图标，我们可以将其替换成自己的图标，方法是使用`--icon`选项。

>`-i <FILE.ico or FILE.exe,ID or FILE.icns or Image or "NONE">`, `--icon <FILE.ico or FILE.exe,ID or FILE.icns or Image or "NONE">`[](https://pyinstaller.org/en/stable/usage.html#cmdoption-i)
>
>FILE.ico: apply the icon to a Windows executable. FILE.exe,ID: extract the icon with ID from an exe. FILE.icns: apply the icon to the .app bundle on Mac OS. If an image file is entered that isn’t in the platform format (ico on Windows, icns on Mac), PyInstaller tries to use Pillow to translate the icon into the correct format (if Pillow is installed). Use “NONE” to not apply any icon, thereby making the OS show some default (default: apply PyInstaller’s icon). This option can be used multiple times.

首先，需要准备好图标文件（`.ico`或`.icns`格式），并将其放到`app.py`同目录下。

<div style="text-align:center">
    <img src="/assets/packaging_12.png" />
</div>

执行以下打包命令：

```bash
 pyinstaller app.py --name "Equation-Solver" --icon "./icon.ico"   --collect-data yapf_third_party --collect-data pyqcodeeditor --add-data "./about.html:./" -y --clean
```

打包完成后，我们就得到了一个带自定义图标的可执行文件了：

<div style="text-align:center">
    <img src="/assets/packaging_13.png" />
</div>

## （五）窗口模式

`pyinstaller`打包应用程序的时候默认使用`-c`选项，因此打开生成的可执行文件时将同时打开一个控制台窗口作为其标准io。若要隐藏该窗口，可以使用`-w`选项。

>`-w`, `--windowed`, `--noconsole`[](https://pyinstaller.org/en/stable/usage.html#cmdoption-w)
>
>Windows and Mac OS X: do not provide a console window for standard i/o. On Mac OS this also triggers building a Mac OS .app bundle. On Windows this option is automatically set if the first script is a ‘.pyw’ file. This option is ignored on *NIX systems.

```bash
pyinstaller app.py -w --name "Equation-Solver" --icon "./icon.ico"   --collect-data yapf_third_party --collect-data pyqcodeeditor --add-data "./about.html:./" -y --clean
```

## （六）单文件模式

`pyinstaller`在打包时，默认会生成一个可执行文件以及一个用于存放其他文件的目录（默认为`_internal`）。`pyinstaller`也支持将所有文件打包成单个可执行文件，方法是使用`-F`选项。

> `-F`, `--onefile`[](https://pyinstaller.org/en/stable/usage.html#cmdoption-F)
>
> Create a one-file bundled executable.

首先，将`dist/`目录清空。然后执行下列命令。

```bash
pyinstaller app.py -F -w --name "Equation-Solver" --icon "./icon.ico"   --collect-data yapf_third_party --collect-data pyqcodeeditor --add-data "./about.html:./" -y --clean
```

打包完成后，`dist/`目录下只有一个可执行文件，其他所有文件都被打包到这个文件中了。

<div style="text-align:center">
    <img src="/assets/packaging_14.png" />
</div>

现在只需要一个文件就可以完成程序的分发了。

<div style="text-align:center">
    <img src="/assets/packaging_15.gif" />
</div>

相比多文件模式，单文件打包的优势主要包括以下两点：

- 方便部署和分发
- 总的体积更小

不足在于应用启动的速度可能会稍慢一些（运行速度不受影响），但是一般不是很明显。

就本示例来说，在启用单文件模式前，所有文件体积加起来有`114MB`左右，而采用单文件模式后，文件体积被压缩到`46.5MB`，可以说效果显著。

## （七）进一步压缩体积的方法

### 1、使用`--strip`选项

按照`pyinstaller`官方的说法，该选项可用于去除可执行文件和共享库中的符号表（在`Windows`下不推荐使用），这可能有助于减少生成文件的体积。

> `-s`, `--strip`[](https://pyinstaller.org/en/stable/usage.html#cmdoption-s)
>
> Apply a symbol-table strip to the executable and shared libs (not recommended for Windows)

### 2、使用`upx`

笔者没有实际尝试这种方法，具体的方法可以参考`pyinstaller`的官方文档：[Using Upx](https://pyinstaller.org/en/stable/usage.html#using-upx)。

## （八）结语

`pyinstaller`提供了丰富的打包选项，本文仅仅对常用的几个选项进行一些说明和演示。开发者可以进一步阅读官方文档，了解更多细节了，打包过程中遇到的绝大多数问题都可以在其中找到解决方法，以下是`pyinstaller`官方文档的地址：[PyInstaller Manual — PyInstaller 6.10.0 documentation](https://pyinstaller.org/en/stable/index.html)。

这里，也贴出本次演示最终的`spec`文件，开发者可以在这个文件基础上进行修改，从而快速得到符合自己项目实际的打包配置文件。

> [`examples/packaging/Equation-Solver.spec`]({{main_branch}}/examples/packaging/Equation-Solver.spec)

```python
# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_data_files

datas = [('./about.html', './')]
datas += collect_data_files('yapf_third_party')
datas += collect_data_files('pyqcodeeditor')


a = Analysis(
    ['app.py'],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='Equation-Solver',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['icon.ico'],
)
```

