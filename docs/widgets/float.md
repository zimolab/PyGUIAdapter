# `float`类型及`FloatSpinBox`控件

## 一、控件类型：FloatSpinBox

> 源码：[pyguiadapter/widgets/basic/floatspin.py]()

用于`float`类型数据的输入，是`float`类型参数的默认控件。

![](../images/floatspin.png)

## 二、配置类型：FloatSpinBoxConfig

> 源码：[pyguiadapter/widgets/basic/floatspin.py]() 

```py
@dataclasses.dataclass(frozen=True)
class FloatSpinBoxConfig(CommonParameterWidgetConfig):
    default_value: float | None = 0.0
    min_value: float = -2147483648.0
    max_value: float = 2147483647.0
    step: float | None = None
    decimals: int | None = None
    prefix: str = ""
    suffix: str = ""
    
```

|   配置项名称    |      类型       |     默认值      |                   说明                   |
| :-------------: | :-------------: | :-------------: | :--------------------------------------: |
| `default_value` | `float \| None` |      `0.0`      |                控件默认值                |
|   `min_value`   |     `float`     | `-2147483648.0` |             控件接受的最大值             |
|   `max_value`   |     `float`     | `2147483647.0`  |             控件接受的最小值             |
|     `step`      | `float \| None` |     `None`      |               单次步进值。               |
|    `prefix`     |      `str`      |      `""`       | 显示在值之前的前缀，默认为空，即无前缀。 |
|    `suffix`     |      `str`      |      `""`       | 显示在值之后的后缀，默认为空，即无后缀。 |
|   `decimals`    |  `int \| None`  |     `None`      |              小数点后的位数              |



## 三、示例

> 源码：[examples/widgets/float_example.py]()



```python
from pyguiadapter.adapter import GUIAdapter
from pyguiadapter.adapter.ucontext import uprint
from pyguiadapter.widgets import FloatSpinBoxConfig


def float_example(float_arg1: float, float_arg2: float, float_arg3: float = 3.14):
    """
    example for **float** and **FloatSpinBox**

    @param float_arg1: this parameter is configured in docstring , see `@params ... @end` block below
    @param float_arg2: this parameter is configured with `run()` via a FloatSpinBoxConfig object
    @param float_arg3: this parameter is configured with `run()` via a dict instance
    @return:

    @params
    [float_arg1]
    default_value = 1.0
    max_value = 100.0
    step = 2.0
    decimals = 3
    prefix = "r: "
    suffix = "%"

    @end

    """
    uprint("float_arg1", float_arg1)
    uprint("float_arg2", float_arg2)
    uprint("float_arg3", float_arg3)
    return float_arg1 + float_arg2 + float_arg3


if __name__ == "__main__":
    adapter = GUIAdapter()

    float_arg2_config = FloatSpinBoxConfig(
        default_value=-0.5, max_value=1.0, step=0.000005, decimals=5, prefix="R: "
    )

    adapter.add(
        float_example,
        widget_configs={
            "float_arg2": float_arg2_config,
            "float_arg3": {
                # this will override the default_value in the function signature
                "default_value": 0.5,
                "max_value": 2.0,
                "step": 0.00001,
                "decimals": 5,
            },
        },
    )
    adapter.run()

```

<img src="../images/Float_example.png" />



---

[参数数据类型及其对应控件](widgets/types_and_widgets.md)
