## （一）概述

开发者可以向 `GUIAdapter`实例中添加多个函数，在此情况下，`PyGUIAdapter`将显示一个`函数选择窗口（FnSelectWindow）`，并以列表的形式展现所有已添加的函数，供用户选择。在函数列表中，将显示函数图标与名称，开发者可以对图标与函数的显示名称进行自定义。同时，在`函数选择窗口（FnSelectWindow）`的右侧，将通过`文档浏览器（Document Browser）`显示当前选中函数的说明文档。

<div style="text-align:center">
    <img src="/assets/fn_select_wind.png" />
</div>

用户可通过双击函数列表中的条目或者点击`选择按钮（Select）`打开目标函数的执行窗口（`FnExecuteWindow`）。

<div style="text-align:center">
    <img src="/assets/fn_select_wind.gif" />
</div>

同时，`PyGUIAdapter`支持函数分组功能，在函数较多时，使用该功能可以使界面更加简洁、直观。

<div style="text-align:center">
    <img src="/assets/fn_groups.gif" />
</div>

下面，围绕`GUIAdapter.add()`函数对上面提到的功能进行详细说明。



## （二）添加多个函数

在调用`GUIAdapter.run()`函数前，开发者可以通过多次调用`GUIAdapter.add()`将多个函数添加到`GUIAdapter`实例中：

> [examples/multiple_function_example.py]({{main_branch}}/examples/multiple_function_example.py)

```python
from pyguiadapter.adapter import GUIAdapter


def function_1(arg: int):
    """
    description of function_1
    """
    pass


def function_2(arg: int):
    """
    description of function_2
    """
    pass


def function_3(arg: int):
    """
    description of function_3
    """
    pass


if __name__ == "__main__":
    adapter = GUIAdapter()
    adapter.add(function_1)
    adapter.add(function_2)
    adapter.add(function_3)
    adapter.run()
```

<div style="text-align:center">
    <img src="/assets/fn_select_wind.gif" />
</div>

所有添加到`GUIAdapter`实例中的函数都会显示在`函数选择窗口（FnSelectWindow）`左侧的函数列表中。函数列表将同时显示函数的名称及图标，如果没有显式地指定函数的图标和名称，`PyGUIAadpter`将使用默认的图标，显示的名称则为函数名。

当用户选中函数列表中的某个条目，双击它或者点击右下方的`Select`按钮，即可进入对应的`函数执行窗口（FnExecuteWindow）`。当用户关闭`函数执行窗口（FnSelectWindow）`，将回到函数选择界面。

## （三）自定义函数图标（`icon`）及名称（`display_name`）

`PyGUIAdapter`允许开发者对函数的图标（`icon`）及其显示名称（`display_name`）进行自定义。为函数设置独特的图标，赋予函数一个更具可读性的名称，将有助于提高界面的观感并增强用户的体验。

>  [examples/custom_icon_and_name_example.py]({{main_branch}}/examples/custom_icon_and_name_example.py)

```python
from pyguiadapter.adapter import GUIAdapter


def function_1(arg: int):
    """
    description of function_1
    """
    pass


def function_2(arg: int):
    """
    description of function_2
    """
    pass


def function_3(arg: int):
    """
    description of function_3
    """
    pass


if __name__ == "__main__":
    adapter = GUIAdapter()
    adapter.add(function_1, display_name="Barcode Generator", icon="ei.barcode")
    adapter.add(function_2, display_name="QRCode Generator", icon="ei.qrcode")
    adapter.add(function_3, display_name="Generator Service", icon="mdi.web")
    adapter.run()

```

<div style="text-align:center">
    <img src="/assets/custom_icon_and_name.png" />
</div>

> 在本例中，使用了字体图标名称作为函数的`icon`，开发者也可以传入图标文件路径。更多详细信息可以参考：[关于图标](icon_type.md)。



## （四）设置函数说明文档

在`函数选择窗口（FnSelectWindow）`和`函数执行窗口（FnExecuteWindow）`中均有专门的区域用于显示函数的说明文档，用于显示函数文档的组件被称为`文档浏览器（DocumentBrowser）`。

默认情况下，`PyGUIAdapter`会自动提取函数文档字符串（`docstring`）中对于函数的描述（包括`long description`和`short description`，但一般不包括参数的描述部分和`@params...@end`块）作为说明文档，格式默认为`Markdown`。比如：

<div style="text-align:center">
    <img src="/assets/docstring_document.png" />
</div>

> [examples/html_docstring__document_example.py]({{main_branch}}/examples/html_docstring__document_example.py)

```python
from pyguiadapter.adapter import GUIAdapter


def function_1(arg1: int, arg2: str, arg3: bool):
    """
    ### Description
    This is the document of the **function_1**. And by default this document will automatically
    appear in the `document area`.

    The format of the document is **Markdown** by default. The **plaintext** and **html** formats are also
    supported.

    ---

    ### Arguments
    This function needs 3 arguments:
    - **arg1**: Balabala....
    - **arg2**: Balabala....
    - **arg3**: Balabala....

    @param arg1:
    @param arg2:
    @param arg3:
    @return:
    """
    pass


if __name__ == "__main__":
    adapter = GUIAdapter()
    adapter.add(function_1)
    adapter.run()

```

除了`markdown`，也可以将文档的格式指定为`html`或`plaintext`。比如：

<div style="text-align:center">
    <img src="/assets/html_docstring.png" />
</div>

> 

```python
from pyguiadapter.adapter import GUIAdapter


def function_2(arg1: int, arg2: str, arg3: bool):
    """
    <h3>Description</h3>
    <p>
    This is the document of the <b>function_2</b>. And by default this document will automatically
    appear in the <strong>document area</strong>.
    </p>
    <p>
    The format of the document is <b>Markdown</b> by default.
    The <b>plaintext</b> and <b>html</b> formats are also supported.
    </p>
    <hr>
    <h3>Arguments</h3>
    <p>This function needs 3 arguments:</p>
    <ul>
    <li><b>arg1</b>: Balabala....</li>
    <li><b>arg2</b>: Balabala....</li>
    <li><b>arg3</b>: Balabala....</li>
    </ul>

    """
    pass


if __name__ == "__main__":
    adapter = GUIAdapter()
    adapter.add(function_2, document_format="html")
    adapter.run()

```

> 提示：`文档浏览器`对`html`的支持有限，仅支持`html4`的子集，具体可以参考Qt官方文档的说明：[Supported HTML Subset | Qt GUI 5.15.17](https://doc.qt.io/qt-5/richtext-html-subset.html#table-cell-attributes)



当然，如果开发者不想将大段文本放到函数的`docstring`中，也可以手动指定函数的说明文档，比如将外部文件作为说明文档：

<div style="text-align:center">
    <img src="/assets/html_document_file.gif" />
</div>

> [examples/html_file_document_example.py]({{main_branch}}/examples/html_file_document_example.py)

```python
from pyguiadapter import utils
from pyguiadapter.adapter import GUIAdapter


def function_3(arg1: int, arg2: str, arg3: bool):
    """

    @param arg1:
    @param arg2:
    @param arg3:
    @return:
    """
    pass


if __name__ == "__main__":
    adapter = GUIAdapter()
    html_doc = utils.read_text_file("document.html")
    adapter.add(function_3, document=html_doc, document_format="html")
    adapter.run()
```



## （五）对函数进行分组

开发者在调用`GUIAdapter.add()`方法添加函数时，可以通过`group`参数指定函数的分组，`PyGUIAdapter`会将相同`group`的函数聚合到一起；对于未指定`group`的函数，`PyGUIAdapter`则会将其放置在默认分组中，该分组的默认名称为`"Main Functions"`。

比如下面这个示例，将函数按照功能分成了三组：编码器函数`Encoders`、解码器函数`Decoders`和其他函数（默认分组）`Main Functions`。

<div style="text-align:center">
    <img src="/assets/function_groups_2.png" />
</div>

<div style="text-align:center">
    <img src="/assets/function_groups.png" />
</div>

> [examples/function_groups_example.py]({{main_branch}}/examples/function_groups_example.py)



```python
from pyguiadapter.adapter import GUIAdapter


def mp4_encoder():
    """
    MP4 Encoder
    """
    pass


def mp3_encoder():
    """
    MP3 Encoder
    """
    pass


def avi_encoder():
    """
    AVI Encoder
    """
    pass


def ogg_encoder():
    """
    OGG Encoder
    """
    pass


def avi_decoder():
    """
    AVI Decoder
    """
    pass


def ogg_decoder():
    """
    OGG Decoder
    """
    pass


def mp3_decoder():
    """
    MP3 Decoder
    """
    pass


def mp4_decoder():
    """
    MP4 Decoder
    """
    pass


def universal_settings():
    """
    Universal Settings
    """
    pass


if __name__ == "__main__":
    adapter = GUIAdapter()
    adapter.add(universal_settings)
    adapter.add(mp4_encoder, group="Encoders")
    adapter.add(mp3_encoder, group="Encoders")
    adapter.add(avi_encoder, group="Encoders")
    adapter.add(ogg_encoder, group="Encoders")
    adapter.add(avi_decoder, group="Decoders")
    adapter.add(ogg_decoder, group="Decoders")
    adapter.add(mp3_decoder, group="Decoders")
    adapter.add(mp4_decoder, group="Decoders")
    adapter.run()
```

