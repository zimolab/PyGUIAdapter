# 参数数据类型及其对应控件

### （一）Python内置类型的默认控件

 

|            控件类型            |     控件配置类型     |    对应数据类型    |             说明             |                   外观                    |
| :----------------------------: | :------------------: | :----------------: | :--------------------------: | :---------------------------------------: |
| [`IntSpinBox`](widgets/int.md) |  `IntSpinBoxConfig`  |       `int`        |    用于输入`int`类型数据     |   ![intspin.png](../images/intspin.png)   |
|         `FloatSpinBox`         | `FloatSpinBoxConfig` |      `float`       |   用于输入`float`类型数据    | ![floatspin.png](../images/floatspin.png) |
|           `BoolBox`            |   `BoolBoxConfig`    |       `bool`       | 用于输入`bool`类型数据，提供 |   ![boolbox.png](../images/boolbox.png)   |
|                                |                      |       `str`        |                              |  ![lineedit.png](../images/lineedit.png)  |
|                                |                      |       `dict`       |                              |                                           |
|                                |                      |       `list`       |                              |                                           |
|                                |                      |      `tuple`       |                              |                                           |
|                                |                      |       `set`        |                              |                                           |
|                                |                      |       `date`       |                              |                                           |
|                                |                      |       `time`       |                              |                                           |
|                                |                      |     `datetime`     |                              |                                           |
|                                |                      |  `typing.Literal`  |                              |                                           |
|                                |                      | `typing.TypedDict` |                              |                                           |
|                                |                      |   `typing.Union`   |                              |                                           |
|                                |                      | `typing.Optional`  |                              |                                           |
|                                |                      |    `typing.Any`    |                              |                                           |
|                                |                      |       `Enum`       |                              |                                           |



### （二）语义化类型（扩展类型）及其控件

