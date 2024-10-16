## 内置参数控件一览

### （一）Python内置类型的默认控件

|                  控件类型                  |        控件配置类型        |                     对应参数类型                      |                             说明                             |                   外观                    |
| :----------------------------------------: | :------------------------: |:-----------------------------------------------:| :----------------------------------------------------------: | :---------------------------------------: |
|       [`IntSpinBox`](widgets/int.md)       |     `IntSpinBoxConfig`     |                      `int`                      |                   用于输入`int`类型数据。                    |   ![intspin.png](/assets/intspin.png)   |
|     [`FloatSpinBox`](widgets/float.md)     |    `FloatSpinBoxConfig`    |                     `float`                     |                  用于输入`float`类型数据。                   | ![floatspin.png](/assets/floatspin.png) |
|        [`BoolBox`](widgets/bool.md)        |      `BoolBoxConfig`       |                     `bool`                      |                   用于输入`bool`类型数据。                   |   ![boolbox.png](/assets/boolbox.png)   |
|        [`LineEdit`](widgets/str.md)        |      `LineEditConfig`      |                      `str`                      |                   用于输入`str`类型数据。                    |  ![lineedit.png](/assets/lineedit.png)  |
|       [`DictEdit`](widgets/dict.md)        |      `DictEditConfig`      | `dict`、`typing.Dict`、`Mapping`、`MutableMapping` |                   用于字典类型数据的输入。                   |          ![](/assets/dict.png)          |
|       [`ListEdit`](widgets/list.md)        |      `ListEditConfig`      |              `list`、`typing.List`               |                   用于列表类型数据的输入。                   |          ![](/assets/list.png)          |
|      [`TupleEdit`](widgets/tuple.md)       |     `TupleEditConfig`      |             `tuple`、`typing.Tuple`              |                   用于元组类型数据的输入。                   |         ![](/assets/tuple.png)          |
|       [`SetEdit`](../widgets/set.md)       |      `SetEditConfig`       |         `set`、`typing.Set`、`MutableSet`         |                   用于集合类型数据的输入。                   |          ![](/assets/set.png)           |
|       [`DateEdit`](widgets/date.md)        |      `DateEditConfig`      |                     `date`                      | 该控件用于输入日期，是python内置`datetime.date`类型参数的默认输入控件。 |       ![](/assets/date_edit.png)        |
|       [`TimeEdit`](widgets/time.md)        |      `TimeEditConfig`      |                     `time`                      | 该控件用于输入日期，是python内置`datetime.time`类型参数的默认输入控件。 |       ![](/assets/time_edit.png)        |
|   [`DateTimeEdit`](widgets/datetime.md)    |    `DateTimeEditConfig`    |                   `datetime`                    | 该控件用于输入日期时间，是python内置`datetime.datetime`类型参数的默认输入控件。 |     ![](/assets/datetime_edit.png)      |
| [`ExclusiveChoiceBox`](widgets/literal.md) | `ExclusiveChoiceBoxConfig` |                `typing.Literal`                 | 用于从一组选项中选择一个选项，是`typing.Literal`类型的默认控件，可以自动提取`Literal`所有给定的字面量并将其作为可选项。 |  ![](/assets/exclusive_choice_box.png)  |
|     [`PyLiteralEdit`](widgets/any.md)      |   `PyLiteralEditConfig`    |      `typing.Any`、`object`、`typing.Union`       | `PyLiteralEdit`是[`BaseCodeEdit`](widgets/base_code_edit.md)的子类，主要用于Python字面量的输入，是`Any`、`object`、`Union`等类型的函数参数的默认输入控件。 `Python字面量`是指`ast.eval_literal()`函数支持任意Python字面量结构，包括：字符串、字节对象、数值、元组、列表、字典、集合、布尔值等。 |          ![](/assets/any.png)           |
|      [`EnumSelect`](widgets/enum.md)       |     `EnumSelectConfig`     |                   `enum.Enum`                   |                用于`Enum`（枚举类型）值的输入                |       ![](/assets/enumselect.png)       |

### （二）语义化类型（扩展类型）及其控件

`语义化类型`是从Python内置类型中扩展而来的类型，可以看作对应内置类型的`“别名”`，在使用上与对应内置类型没有区别。其主要作用在于，提供区别于对应内置类型的控件，以满足特定场景下的输入需求。比如`int_slider_t`是内置`int`类型的语义化类型（扩展类型），在使用上与`int`类型完全一致，但它提供了一个类似滑动条的输入控件，而不是`IntSpinBox`。通过合理使用语义化类型，开发者可以构建出界面更加丰富，用户交互体验更佳的应用程序。

以下是`PyGUIAdapter`提供的语义化类型及其对应的控件类型列表。开发者可以跳转到对应的页面，查看控件的用法和使用示例。



> `PyGUIAdapter`提供的语义化类型在：[pyguiadapter/types]()中定义。



|                    控件类型                    |      控件配置类型       |      对应数据类型      |                             说明                             |               外观                |
| :--------------------------------------------: | :---------------------: | :--------------------: | :----------------------------------------------------------: | :-------------------------------: |
|       [`IntLineEdit`](widgets/int_t.md)        |   `IntLineEditConfig`   |        `int_t`         | `int_t`扩展自`int`，可以看作是`int`类型的别名。`PyGUIAdapter`为该类型提供了一个单行文本输入框样式的输入组件，但于与一般单行文本输入框标题，该类型的输入组件只允许用户输入整数文本。 |     ![](/assets/int_t.png)      |
|     [`FloatLineEdit`](widgets/float_t.md)      |  `FloatLineEditConfig`  |       `float_t`        | `float_t`扩展自`float`，可以看作是`float`类型的别名。`PyGUIAdapter`为该类型提供了一个单行文本输入框样式的输入组件，但于与一般单行文本输入框标题，该类型的输入组件只允许用户输入浮点数文本。 |    ![](/assets/float_t.png)     |
|        [`TextEdit`](widgets/text_t.md)         |    `TextEditConfig`     |        `text_t`        | `text_t`扩展自`str`，可以看作是`str`类型的别名。`PyGUIAdapter`为该类型提供了一个多行文本输入框，允许用户输入多行文本。 |     ![](/assets/text_t.png)     |
|      [`Slider`](widgets/int_slider_t.md)       |     `SliderConfig`      |     `int_slider_t`     | `int_slider_t`扩展自`int`，可以看作是`int`类型的别名。与其他`int`不同，`PyGUIAdapter`为该类型提供了滑动块形式的输入控件。 |  ![](/assets/int_slider_t.png)  |
|        [`Dial`](widgets/int_dial_t.md)         |      `DialConfig`       |      `int_dial_t`      | `int_dial_t`扩展自`int`，可以看作是`int`类型的别名。与其他`int`不同，`PyGUIAdapter`为该类型提供了刻度盘形式的输入控件。 |   ![](/assets/int_dial_t.png)   |
|      [`ColorPicker`](widgets/color_t.md)       |   `ColorPickerConfig`   |       `color_t`        | `color_t`扩展自`object`，代表颜色类型的数据，实际支持的类型包括`tuple`（3元素或4元素元组）、`str`、`QColor`，发者可以选择颜色的表示方式。`PyGUIAdapter`为该类型提供了一个颜色选择器。 |    ![](/assets/color_t.png)     |
|       [`ChoiceBox`](widgets/choice_t.md)       |    `ChoiceBoxConfig`    |       `choice_t`       | 该类型扩展自`object`，`PyGUIAdapter`为该类型提供了一个下拉选择框，用户可以从一组选项中选择其中一个。 |    ![](/assets/choice_t.png)    |
|    [`MultiChoiceBox`](widgets/choices_t.md)    | `MultiChoiceBoxConfig`  |      `choices_t`       |      该类型扩展自`list`，用于从一组对象中选择多个对象。      |   ![](/assets/choices_t.png)    |
| [`KeySequenceEdit`](widgets/key_sequence_t.md) | `KeySequenceEditConfig` |    `key_sequence_t`    |          `key_sequence_t`扩展自`str`，代表快捷键。           | ![](/assets/key_sequence_t.png) |
|   [`PlainDictEdit`](widgets/plain_dict_t.md)   |  `PlainDictEditConfig`  |     `plain_dict_t`     | `plain_dict_t`类型扩展自`dict`，用于`Dict[key, int|bool|float|str|list|dict]`类型数据的输入。 |  ![](/assets/plain_dict_t.png)  |
|  [`StringListEdit`](widgets/string_list_t.md)  | `StringListEditConfig`  |    `string_list_t`     | `string_list_t`扩展自`list`，用于`List[str]`类型数据的输入。 | ![](/assets/string_list_t.png)  |
|        [`JsonEdit`](widgets/json_obj_t)        |    `JsonEditConfig`     |      `json_obj_t`      | `json_obj_t`扩展自`object`，用于json类型数据的输入。用户在控件上输入的文本将通过`json.loads`转换为对应的Python对象。 |   ![](/assets/json_obj_t.png)   |
|     [`DirSelect`](widgets/directory_t.md)      |    `DirSelectConfig`    | `directory_t`、`dir_t` | `directory_t`扩展自`str`，代表一个目录路径，`PyGUIAdapter`为该类型提供了一个文件选择对话框用于选择目录。 |  ![](/assets/directory_t.png)   |
|       [`FileSelect`](widgets/file_t.md)        |   `FileSelectConfig`    |        `file_t`        | `file`扩展自`str`，代表一个文件路径，`PyGUIAdapter`为该类型提供了一个文件选择对话框用于选择文件。 |     ![](/assets/file_t.png)     |
|    [`MultiFileSelect`](widgets/files_t.md)     | `MultiFileSelectConfig` |       `files_t`        | `files`扩展自`list`，代表一组文件路径，`PyGUIAdapter`为该类型提供了一个文件选择对话框用于选择多个文件。 |    ![](/assets/files_t.png)     |

