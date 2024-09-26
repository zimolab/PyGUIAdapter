# `MultiFileSelect`控件

## 一、控件类型：`MultiFileSelect`

> 源码: [`pyguiadapter/widgets/extend/fileselect.py`]()

<img src="../images/files_t.png" />

`files`扩展自`list`，代表一组文件路径，`PyGUIAdapter`为该类型提供了一个文件选择对话框用于选择多个文件。

## 二、配置类型：`MultiFileSelectConfig`

> 源码: [`pyguiadapter/widgets/extend/fileselect.py`]()

```python
@dataclasses.dataclass(frozen=True)
class MultiFileSelectConfig(CommonParameterWidgetConfig):
    default_value: List[str] = dataclasses.field(default_factory=list)
    placeholder: str = ""
    dialog_title: str = ""
    start_dir: str = ""
    filters: str = ""
    file_separator: str = ";;"
    select_button_text: str = "..."
    clear_button: bool = False

    @classmethod
    def target_widget_class(cls) -> Type["MultiFileSelect"]:
        return MultiFileSelect

```

| 配置项名称           | 类型        | 默认值  | 说明                           |
| -------------------- | ----------- | ------- | ------------------------------ |
| `default_value`      | `List[str]` | `[]`    | 控件默认值。                   |
| `placeholder`        | `str`       | `""`    | 无输入时的占位符文本。         |
| `dialog_title`       | `str`       | `""`    | 选择文件对话框的标题。         |
| `start_dir`          | `str`       | `""`    | 选择文件对话框的起始路径。     |
| `filters`            | `str`       | `""`    | 选择文件对话框的文件名过滤器。 |
| `file_separator`     | `str`       | `";;"`  | 文件名分隔符。                 |
| `select_button_text` | `str`       | `"..."` | 选择文件按钮标题。             |
| `clear_button`       | `bool`      | `False` | 是否显示编辑框的清除按钮。     |

## 三、示例

> 源码：[examples/widgets/files_t_example.py]()

```python
import os.path

from pyguiadapter.adapter import GUIAdapter
from pyguiadapter.adapter.ucontext import uprint
from pyguiadapter.widgets import MultiFileSelectConfig
from pyguiadapter.extend_types import files_t


def files_t_example(arg1: files_t, arg2: files_t, arg3: files_t):
    """
    example for type **files_t** and **MultiFileSelect** widget

    @param arg1: description for arg1
    @param arg2: description for arg2
    @param arg3: description for arg3

    @params
    [arg3]
    placeholder = "select files"
    @end

    """
    uprint("arg1:", arg1)
    uprint("arg2:", arg2)
    uprint("arg3:", arg3)


if __name__ == "__main__":
    arg1_conf = MultiFileSelectConfig(
        placeholder="input files here",
        filters="Text files(*.txt);;All files(*.*)",
        dialog_title="Open Files",
    )
    arg2_conf = MultiFileSelectConfig(
        default_value=[os.path.abspath(__file__)],
        start_dir=os.path.expanduser("~"),
        clear_button=True,
    )
    adapter = GUIAdapter()
    adapter.add(files_t_example, widget_configs={"arg1": arg1_conf, "arg2": arg2_conf})
    adapter.run()

```

<img src="../images/files_t_example.png" />

---

[参数数据类型及其对应控件](widgets/types_and_widgets.md)