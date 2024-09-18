# `SetEdit`控件

## 一、控件类型：`SetEdit`

> 源码: [`pyguiadapter/widgets/basic/setedit.py`]()



`SetEdit`是[`PyLiteralEdit`](widgets/any.md)的子类，主要用于Python列表类型数据的输入，是`set`、`typing.Set`、`MutableSet`等类型的函数参数的默认输入控件。

<img src="../images/set.png" />   <img src="../images/set_editor.png" />

## 二、配置类型：`SetEditConfig`

> 源码: [`pyguiadapter/widgets/basic/setedit.py`]()

```python
@dataclasses.dataclass(frozen=True)
class SetEditConfig(PyLiteralEditConfig):
    default_value: set | None = dataclasses.field(default_factory=_set_default)
    initial_text: str = "()"

    @classmethod
    def target_widget_class(cls) -> Type["SetEdit"]:
        return SetEdit

```

| 配置项名称      | 类型          | 默认值 |
| --------------- | ------------- | ------ |
| `default_value` | `set \| None` | `{}`   |

`SetEditConfig`继承自[`PyLiteralEditConfig`](widgets/any.md)，其可配置项，可以参考：

- [`PyLiteralEditConfig`](widgets/any.md)
- [`BaseCodeEditConfig`](widgets/base_code_edit.md)



## 三、示例

> 源码：[examples/widgets/set_example.py]()

```python
from typing import Set, MutableSet

from pyguiadapter.adapter import GUIAdapter
from pyguiadapter.adapter.ucontext import uprint
from pyguiadapter.widgets import SetEditConfig


def set_example(arg1: set, arg2: Set, arg3: MutableSet):
    """
    example for **SetEdit** for **set-like** types
    """
    uprint("arg1: ", arg1)
    uprint("arg2: ", arg2)
    uprint("arg3: ", arg3)


if __name__ == "__main__":
    arg1_conf = SetEditConfig(
        default_value={1, 2, 3},
    )
    arg2_conf = SetEditConfig(
        default_value={"a", "b", 1, 2},
    )
    arg3_conf = {
        "default_value": {1, 2, 3, (1, 2, 3, 4)},
    }
    adapter = GUIAdapter()
    adapter.add(
        set_example,
        widget_configs={
            "arg1": arg1_conf,
            "arg2": arg2_conf,
            "arg3": arg3_conf,
        },
    )
    adapter.run()
```

<img src="../images/set_example.png" />



---

[参数数据类型及其对应控件](widgets/types_and_widgets.md)