#  参数数据类型及其对应控件

### （一）Python内置类型的默认控件

|                  控件类型                  |        控件配置类型        |              对应数据类型              |                        说明                        |                   外观                    |
| :----------------------------------------: | :------------------------: | :------------------------------------: | :------------------------------------------------: | :---------------------------------------: |
|       [`IntSpinBox`](widgets/int.md)       |     `IntSpinBoxConfig`     |                 `int`                  |               用于输入`int`类型数据                |   ![intspin.png](../images/intspin.png)   |
|     [`FloatSpinBox`](widgets/float.md)     |    `FloatSpinBoxConfig`    |                `float`                 |              用于输入`float`类型数据               | ![floatspin.png](../images/floatspin.png) |
|        [`BoolBox`](widgets/bool.md)        |      `BoolBoxConfig`       |                 `bool`                 |               用于输入`bool`类型数据               |   ![boolbox.png](../images/boolbox.png)   |
|        [`LineEdit`](widgets/str.md)        |      `LineEditConfig`      |                 `str`                  |               用于输入`str`类型数据                |  ![lineedit.png](../images/lineedit.png)  |
|               [`DictEdit`]()               |      `DictEditConfig`      |       `dict`、`typing.TypedDict`       |                                                    |                                           |
|               [`ListEdit`]()               |      `ListEditConfig`      |                 `list`                 |                                                    |                                           |
|              [`TupleEdit`]()               |     `TupleEditConfig`      |                `tuple`                 |                                                    |                                           |
|               [`SetEdit`]()                |      `SetEditConfig`       |                 `set`                  |                                                    |                                           |
|               [`DateEdit`]()               |      `DateEditConfig`      |                 `date`                 |                                                    |       ![](../images/date_edit.png)        |
|               [`TimeEdit`]()               |      `TimeEditConfig`      |                 `time`                 |                                                    |       ![](../images/time_edit.png)        |
|             [`DateTimeEdit`]()             |    `DateTimeEditConfig`    |               `datetime`               |                                                    |     ![](../images/datetime_edit.png)      |
| [`ExclusiveChoiceBox`](widgets/literal.md) | `ExclusiveChoiceBoxConfig` |            `typing.Literal`            | 用于从`typing.Literal`提供的一组选项中选择一个选项 |  ![](../images/exclusive_choice_box.png)  |
|            [`PyLiteralEdit`]()             |   `PyLiteralEditConfig`    | `typing.Any`、`object`、`typing.Union` |                                                    |                                           |
|      [`EnumSelect`](widgets/enum.md)       |     `EnumSelectConfig`     |              `enum.Enum`               |           用于`Enum`（枚举类型）值的输入           |       ![](../images/enumselect.png)       |

### （二）语义化类型（扩展类型）及其控件

|       控件类型        |      控件配置类型       | 对应数据类型 | 说明 | 外观 |
| :-------------------: | :---------------------: | :----------: | :--: | :--: |
|   [`IntLineEdit`]()   |   `IntLineEditConfig`   |              |      |      |
|  [`FloatLineEdit`]()  |  `FloatLineEditConfig`  |              |      |      |
|     [`Slider`]()      |     `SliderConfig`      |              |      |      |
|      [`Dial`]()       |      `DialConfig`       |              |      |      |
|   [`ColorPicker`]()   |   `ColorPickerConfig`   |              |      |      |
|    [`ComboBox`]()     |    `ComboBoxConfig`     |              |      |      |
| [`KeySequenceEdit`]() | `KeySequenceEditConfig` |              |      |      |
| [`MultiChoiceBox`]()  | `MultiChoiceBoxConfig`  |              |      |      |
|  [`PlainDictEdit`]()  |  `PlainDictEditConfig`  |              |      |      |
| [`StringListEdit`]()  | `StringListEditConfig`  |              |      |      |
|    [`JsonEdit`]()     |    `JsonEditConfig`     |              |      |      |
|    [`DirSelect`]()    |    `DirSelectConfig`    |              |      |      |
|   [`FileSelect`]()    |   `FileSelectConfig`    |              |      |      |
| [`MultiFileSelect`]() | `MultiFileSelectConfig` |              |      |      |

