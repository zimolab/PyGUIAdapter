## （一）概述

开发者有时需要在函数运行过程中与用户进行交互，比如弹出消息对话框，向用户展示一些信息；请求用户对某些操作进行确认；或者是要求用户输入某些数据。对此，`PyGUIAdapter`提供了支持。

运行中的交互，总的来说，可以分为两类：一是展示信息，二是请求输入数据。下面将分别对这两方面进行阐述。



## （二）消息对话框

消息对话框相关的API定义在[`pyguiadapter.adapter.udialog`]({{main_branch}}/pyguiadater/adapter/udialog.py)模块中，可以通过如下方式导入该模块

```python
from pyguiadapter.adapter import udialog
```

消息对话框相关的API可以参考以下文档：

- [**pyguiadapter.adapter.udialog**](apis/pyguiadapter.adapter.udialog.md)

### 1、标准消息对话框

`PyGUIAdapter`提供了四种标准的消息对话框，可以用于展示不同级别的消息。

- **Information消息对话框**：用于展示一般性信息。

```python
show_info_messagebox()
```

- **Warning消息对话框：**用于展示警告信息。

```python
show_warning_messagebox()
```

- **Critical消息对话框：**用于展示严重错误信息。

```python
show_critical_messagebox()
```

- **Question对话框：**用于展示问询信息，并且可以获得问询结果。

```python
show_question_messagebox()
```

下面是一个综合的示例：

```python
from pyguiadapter.adapter import GUIAdapter
from pyguiadapter.adapter import udialog
from pyguiadapter.adapter.ucontext import uprint
from pyguiadapter.extend_types import text_t
from pyguiadapter.utils import messagebox


def dialog_example(
    info_message: text_t,
    warning_message: text_t,
    error_message: text_t,
    question_message: text_t,
):
    if info_message:
        udialog.show_info_messagebox(
            text=info_message,
            title="Information",
            buttons=messagebox.Ok | messagebox.No,
            default_button=messagebox.Ok,
        )

    if warning_message:
        udialog.show_warning_messagebox(
            text=warning_message,
            title="Warning",
            buttons=messagebox.Ok | messagebox.No,
            default_button=messagebox.Ok,
        )

    if error_message:
        udialog.show_critical_messagebox(
            text=error_message,
            title="Error",
            buttons=messagebox.Ok | messagebox.No,
            default_button=messagebox.Ok,
        )

    if question_message:
        answer = udialog.show_question_messagebox(
            text=question_message,
            title="Question",
            buttons=messagebox.Yes | messagebox.No,
            default_button=messagebox.No,
        )
        if answer == messagebox.Yes:
            uprint("Your Choice: Yes")
            udialog.show_info_messagebox("You Choose Yes!", title="Answer")
        else:
            uprint("Your Choice: No")
            udialog.show_info_messagebox("You Choose No!", title="Answer")


if __name__ == "__main__":
    adapter = GUIAdapter()
    adapter.add(dialog_example)
    adapter.run()

```

<div style="text-align:center">
    <img src="/assets/udialog_demo.gif" />
</div>

### 2、长文本消息对话框

`PyGUIAdapter`还提供了两种用于展示长文本内容的消息对话框：

- 直接展示长文本字符串

```python
show_text_content()
```

- 展示文本文件内容

```python
show_text_file()
```

一个简单的示例：

```python
import os.path
from typing import Literal

from pyguiadapter.adapter import GUIAdapter
from pyguiadapter.adapter import udialog
from pyguiadapter.exceptions import ParameterError
from pyguiadapter.extend_types import text_t, file_t
from pyguiadapter.utils import messagebox


def show_text_context_example(
    content: text_t, text_format: Literal["markdown", "plaintext", "html"] = "markdown"
):
    if content:
        udialog.show_text_content(
            title="Hello",
            text_content=content,
            text_format=text_format,
            buttons=messagebox.DialogButtonYes | messagebox.DialogButtonNo,
            size=(600, 400),
        )


def show_text_file_example(
    text_file: file_t,
    text_format: Literal["markdown", "plaintext", "html"] = "markdown",
):
    """
    Show text content of the file

    @param text_file: the path of the text file
    @param text_format: the format of the text file
    @return:

    @params
    [text_file]
    filters = "Text files(*.txt);;Markdown files(*.md);;HTML files(*.html);;All files(*.*)"
    @end
    """
    text_file = text_file.strip()
    if not text_file:
        raise ParameterError("text_file", "text_file is empty!")

    if not os.path.isfile(text_file):
        udialog.show_critical_messagebox(text="File not found", title="Error")
        return
    filename = os.path.basename(text_file)
    if text_file:
        udialog.show_text_file(
            text_file=text_file,
            text_format=text_format,
            title=f"View - {filename}",
            size=(600, 400),
        )


if __name__ == "__main__":
    adapter = GUIAdapter()
    adapter.add(show_text_context_example)
    adapter.add(show_text_file_example)
    adapter.run()
```

<div style="text-align:center">
    <img src="/assets/udialog_demo_2.gif" />
</div>

<div style="text-align:center">
    <img src="/assets/udialog_demo_3.gif" />
</div>

### 3、自定义消息对话框

> 为了实现自定义对话框，开发者需要掌握一定`pyqt`或`pyside`开发知识

如果`PyGUIAdapter`内置的消息对话框不能满足需要，开发者也可以自定义消息对话框。一般流程如下：

**1、子类化`pyguiadater.adapter.BaseCustomDialog`类，创建自定义对话框类**

在自定义对话框类中，开发者需实现`get_result()`抽象方法，后续，开发者可以在调用自定义对话框后获取该方法的返回值。

**2、调用`udialog.show_custom_dialog()`弹出自定义对话框**

```python
def show_custom_dialog(
    dialog_class: Type[BaseCustomDialog], **kwargs
) -> Any:
    ...
```

`udialog.show_custom_dialog()`的第一个参数是自定义对话框类，第一个参数之后的关键字参数将作为自定义对话框`__init__()`函数的参数。`udialog.show_custom_dialog()`函数将返回`get_result()`方法的返回值。

下面给出一个自定义消息对话框的示例：

```python
from datetime import date, datetime
from typing import Any
from uuid import uuid1

from qtpy.QtWidgets import QWidget, QVBoxLayout, QLabel, QDialogButtonBox

from pyguiadapter.adapter import GUIAdapter, BaseCustomDialog
from pyguiadapter.adapter import udialog
from pyguiadapter.adapter.ucontext import uprint
from pyguiadapter.exceptions import ParameterError


class UserInfoDialog(BaseCustomDialog):
    def __init__(
        self,
        parent: QWidget,
        username: str,
        nickname: str,
        user_id: str,
        birthdate: date,
        join_time: datetime,
        **kwargs,
    ):
        super().__init__(parent, **kwargs)

        self.setWindowTitle("Confirm")

        self._confirmed = False
        self._user_info = {
            "username": username,
            "nickname": nickname,
            "user_id": user_id,
            "birthdate": birthdate,
            "join_time": join_time,
        }

        self._button_box = QDialogButtonBox(self)
        self._button_box.setStandardButtons(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        )
        self._button_box.accepted.connect(self._on_accepted)
        self._button_box.rejected.connect(self._on_rejected)

        layout = QVBoxLayout()
        username_label = QLabel(self)
        username_label.setText(f"username: {username}")
        layout.addWidget(username_label)
        nickname_label = QLabel(self)
        nickname_label.setText(f"nickname: {nickname}")
        layout.addWidget(nickname_label)
        user_id_label = QLabel(self)
        user_id_label.setText(f"user_id: {user_id}")
        layout.addWidget(user_id_label)
        birthdate_label = QLabel(self)
        birthdate_label.setText(f"birthdate: {birthdate}")
        layout.addWidget(birthdate_label)
        join_time_label = QLabel(self)
        join_time_label.setText(f"join_time: {join_time}")
        layout.addWidget(join_time_label)
        layout.addWidget(self._button_box)
        self.setLayout(layout)

    def get_result(self) -> Any:
        if self._confirmed:
            return self._user_info
        return None

    def _on_accepted(self) -> None:
        self._confirmed = True
        self.accept()

    def _on_rejected(self) -> None:
        self._confirmed = False
        self.reject()


def add_user_example(
    username: str,
    nickname: str,
    user_id: str,
    birth_date: date,
    join_time: datetime,
):
    if not username:
        raise ParameterError("username", "username is empty")

    if not user_id:
        udialog.show_warning_messagebox(
            "user_id is empty, a random one will be generated!"
        )
        user_id = uuid1().hex

    result = udialog.show_custom_dialog(
        UserInfoDialog,
        username=username,
        nickname=nickname,
        user_id=user_id,
        birthdate=birth_date,
        join_time=join_time,
    )
    if result is not None:
        udialog.show_info_messagebox(f"user added!")
        uprint(result)
        return
    udialog.show_info_messagebox(f"user not added!")


if __name__ == "__main__":
    adapter = GUIAdapter()
    adapter.add(add_user_example)
    adapter.run()
```

<div style="text-align:center">
    <img src="/assets/udialog_demo_4.gif" />
</div>



## （三）输入对话框

输入对话框相关API在[`pyguiadapter.adapter.uinput`]({{main_branch}}/pyguiadapter/adapter/uinput.py)模块中定义。

输入对话框相关的API可以参考以下文档：

- [**pyguiadapter.adapter.uinput**](apis/pyguiadapter.adapter.uinput.md)

#### 1、内置输入对话框类型

`PyGUIAdapter`内置了多种类型的输入对话框，用以输入不同类型的数据，包括：

- `get_string()`
- `get_text()`
- `get_int()`
- `get_float()`
- `get_selected_item()`
- `get_color()`
- `get_json_object()`
- `get_py_literal()`
- `get_existing_directory()`
- `get_open_file()`
- `get_open_files()`
- `get_save_file()`

下面是一个综合的示例：

```python
from pyguiadapter.adapter import GUIAdapter
from pyguiadapter.adapter import uinput
from pyguiadapter.adapter.ucontext import uprint
from pyguiadapter.extend_types import choices_t


# noinspection SpellCheckingInspection
def uinput_example(inputs: choices_t):
    """
    Example of getting user inputs inside the function
    @param inputs: choose what you want to get from user
    @return:

    @params
    [inputs]
    choices = ["int", "str", "text", "float", "item", "color", "dir", "file", "save_file", "files", "json object", "python literal"]
    columns = 2
    @end
    """
    if "int" in inputs:
        value = uinput.get_int(title="Input Integer", label="Enter an integer:")
        uprint("User inputs: ", value)
    if "str" in inputs:
        value = uinput.get_string(title="Input Text", label="Enter a string:")
        uprint("User inputs: ", value)
    if "text" in inputs:
        value = uinput.get_text(title="Input Text", label="Enter a string:")
        uprint("User inputs: ", value)
    if "float" in inputs:
        value = uinput.get_float(title="Input Float", label="Enter a float:")
        uprint("User inputs: ", value)

    if "item" in inputs:
        value = uinput.get_selected_item(
            items=["Item 1", "Item 2", "Item 3", "Item 4"],
            title="Select Item",
            label="Select an item:",
        )
        uprint("User inputs: ", value)
    if "color" in inputs:
        value = uinput.get_color(title="Select Color", alpha_channel=True)
        uprint("User inputs: ", value)
    if "dir" in inputs:
        value = uinput.get_existing_directory(title="Select Directory")
        uprint("User inputs: ", value)
    if "file" in inputs:
        value = uinput.get_open_file(title="Select File")
        uprint("User inputs: ", value)
    if "save_file" in inputs:
        value = uinput.get_save_file(title="Select File")
        uprint("User inputs: ", value)
    if "files" in inputs:
        value = uinput.get_open_files(title="Select Files")
        uprint("User inputs: ", value)
    if "json object" in inputs:
        value = uinput.get_json_object(title="Input Json Object")
        uprint("User inputs: ", value, f" {type(value)}")
    if "python literal" in inputs:
        value = uinput.get_py_literal(title="Input Python Literal")
        uprint("User inputs: ", value, f" {type(value)}")


if __name__ == "__main__":
    adapter = GUIAdapter()
    adapter.add(uinput_example)
    adapter.run()
```

<div style="text-align:center">
    <img src="/assets/uinput_example.gif" />
</div>

### 2、自定义输入对话框

若内置的输入对话框无法满足开发者需求，开发者也可以创建并使用自定义输入对话框。

#### （1）大致步骤

**第一步：实现自定义输入对话框**

自定义输入对话框类需继承自[`pyguiadapter.utils.inputdialog.UniversalInputDialog`]({{main_branch}}/pyguiadapter/utils/inputdialog.py)类。开发者必须实现以下两个抽象方法。

**`create_main_widget()`方法**

```
@abstractmethod
def create_main_widget(self) -> QWidget:
    pass
```

开发者需在该方法中创建输入对话框的主控件并将其返回。所谓`主控件（main widget）`是指下图中使用红框标注的位置：

<div style="text-align:center">
    <img src="/assets/custom_input_dialog_main_widget.png" />
</div>

**`get_result()`方法**

该方法用于返回用户在对话框中输入的值。

```python
    @abstractmethod
    def get_result(self) -> Any:
        pass
```

**第二步：弹出自定义输入对话框**

实现自定义输入对话框后，开发者可以调用`uinput.get_custom_input()`函数弹出对话框并获取用户输入值。

```python
def get_custom_input(
    input_dialog_class: Type[UniversalInputDialog],
    **input_dialog_args,
) -> Any:
    ...
```

`get_custom_input()`函数的第一个参数`input_dialog_class`是自定义输入对话框类，第二个参数则是要传递给自定义输入对话框类构造函数的参数。

关于`get_custom_input()`函数的返回值，存在以下两种情况：

（1）若自定义输入对话框被`reject`，则`get_custom_input()`函数返回`None`

（2）若自定义输入对话框被`accept`，则`get_custom_input()`函数返回`get_result()`方法的返回值。



#### （2）实例

下面，通过一个实际的例子来演示如何创建和使用自定义输入对话框。这次我们选择用QT提供的可视化设计工具`QT设计师`来完成自定义输入对话框的主控件的设计和布局。

假设要为以下类型创建自定义输入对话框：

```python
@dataclasses.dataclass
class UserInfo:
    username: str
    birthday: date
    address: str
    email: str
    phone: str
    description: str
```

**第一步：**创建对应的`自定义输入对话框类`，类名为`UserInfoDialog`。

```python
class UserInfoDialog(UniversalInputDialog):

    def __init__(
        self,
        parent: Optional[QWidget],
        title: str = "",
        icon: IconType = None,
        size: Tuple[int, int] = (400, 300),
        ok_button_text: str = "Ok",
        cancel_button_text: Optional[str] = "Cancel",
        **kwargs
    ):
        super().__init__(
            parent,
            title=title,
            icon=icon,
            size=size,
            ok_button_text=ok_button_text,
            cancel_button_text=cancel_button_text,
            **kwargs
        )

    def get_result(self) -> Any:
        pass

    def create_main_widget(self) -> QWidget:
        pass
```

`create_main_widget()`和`get_result()`目前都还是未实现的状态，后面我们将逐步实现它们。同时，读者可能已经注意到，`UserInfoDialog`构造函数中有一些参数，这些参数均来自其父类`UniversalInputDialog`，可以直接从父类构造函数复制过来。

现在，向`UserInfoDialog`类的构造函数中添加一个参数：`initial_user_info`，这个参数表示初始的`UserInfo`对象，后续将用于为控件设置初始值。现在`UserInfoDialog`的构造函数如下：

```python
class UserInfoDialog(UniversalInputDialog):
    def __init__(
        self,
        parent: Optional[QWidget],
        title: str = "",
        icon: IconType = None,
        size: Tuple[int, int] = (400, 300),
        ok_button_text: str = "Ok",
        cancel_button_text: Optional[str] = "Cancel",
        initial_user_info: Optional[UserInfo] = None,
        **kwargs
    ):
        self._initial_user_info: Optional[UserInfo] = initial_user_info
        super().__init__(
            parent,
            title=title,
            icon=icon,
            size=size,
            ok_button_text=ok_button_text,
            cancel_button_text=cancel_button_text,
            **kwargs
        )
    ...
```



**第二步**：创建`主控件`，实现`create_main_widget()`函数。

前面说过，这次选择使用`QT设计师`而不是手动写代码的方式来实现主控件。

根据`UserInfo`的字段信息，在`QT设计师`中拖拽合适的控件，完成布局，并将布局好的界面保存为`.ui`文件，这里我们将其命名为[`user_info_dialog_main_widget.ui`]({{main_branch}}/examples/user_info_dialog_main_widget.ui)，将该文件与`UserInfoDialog`源码文件放在同一目录下。

> 我们需要在`QT设计师`中为输入控件合理设置对象名称（objectName），以便后续在代码中引用它们。在本示例中，这些控件的名称如下图所示：
>
> <div style="text-align:center">
>     <img src="/assets/main_widget_names.png" />
> </div>
>
> 

现在需要在`create_main_widget()`中加载`.ui`文件，获取各字段对应的输入控件，并根据`inital_user_info`设置其初始值，最后返回最外层的控件。

```python
    ...
    def create_main_widget(self) -> QWidget:
        ui_file = "user_info_dialog_main_widget.ui"
        # create widget from ui file
        main_widget = loadUi(ui_file)

        # obtain input widgets for UserInfo fields and set its initial values from initial_user_info
        self._username_edit = main_widget.findChild(QLineEdit, "username_edit")
        if self._initial_user_info:
            self._username_edit.setText(self._initial_user_info.username)

        self._birthday_edit = main_widget.findChild(QDateEdit, "birthday_edit")
        if self._initial_user_info:
            self._birthday_edit.setDate(self._initial_user_info.birthday)

        self._address_edit = main_widget.findChild(QLineEdit, "address_edit")
        if self._initial_user_info:
            self._address_edit.setText(self._initial_user_info.address)

        self._email_edit = main_widget.findChild(QLineEdit, "email_edit")
        if self._initial_user_info:
            self._email_edit.setText(self._initial_user_info.email)

        self._phone_edit = main_widget.findChild(QLineEdit, "phone_edit")
        if self._initial_user_info:
            self._phone_edit.setText(self._initial_user_info.phone)

        self._description_edit = main_widget.findChild(QTextEdit, "description_edit")
        if self._initial_user_info:
            self._description_edit.setText(self._initial_user_info.description)

        return main_widget
```

为了代码的其他地方引用方便，我们可以在构造函数中预先定义`self._username_edit`、`self._birthday_edit`等成员变量。现在，`UserInfoDialog`类的代码如下：

```python
class UserInfoDialog(UniversalInputDialog):
    def __init__(
        self,
        parent: Optional[QWidget],
        title: str = "",
        icon: IconType = None,
        size: Tuple[int, int] = (400, 300),
        ok_button_text: str = "Ok",
        cancel_button_text: Optional[str] = "Cancel",
        initial_user_info: Optional[UserInfo] = None,
        **kwargs
    ):
        self._description_edit: Optional[QTextEdit] = None
        self._phone_edit: Optional[QLineEdit] = None
        self._email_edit: Optional[QLineEdit] = None
        self._address_edit: Optional[QLineEdit] = None
        self._birthday_edit: Optional[QDateEdit] = None
        self._username_edit: Optional[QLineEdit] = None
        self._initial_user_info: Optional[UserInfo] = initial_user_info
        super().__init__(
            parent,
            title=title,
            icon=icon,
            size=size,
            ok_button_text=ok_button_text,
            cancel_button_text=cancel_button_text,
            **kwargs
        )

    def get_result(self) -> Any:
        pass

    def create_main_widget(self) -> QWidget:
        ui_file = "user_info_dialog_main_widget.ui"
        # create widget from ui file
        main_widget = loadUi(ui_file)

        # obtain input widgets for UserInfo fields and set its initial values from initial_user_info
        self._username_edit = main_widget.findChild(QLineEdit, "username_edit")
        if self._initial_user_info:
            self._username_edit.setText(self._initial_user_info.username)

        self._birthday_edit = main_widget.findChild(QDateEdit, "birthday_edit")
        if self._initial_user_info:
            self._birthday_edit.setDate(self._initial_user_info.birthday)

        self._address_edit = main_widget.findChild(QLineEdit, "address_edit")
        if self._initial_user_info:
            self._address_edit.setText(self._initial_user_info.address)

        self._email_edit = main_widget.findChild(QLineEdit, "email_edit")
        if self._initial_user_info:
            self._email_edit.setText(self._initial_user_info.email)

        self._phone_edit = main_widget.findChild(QLineEdit, "phone_edit")
        if self._initial_user_info:
            self._phone_edit.setText(self._initial_user_info.phone)

        self._description_edit = main_widget.findChild(QTextEdit, "description_edit")
        if self._initial_user_info:
            self._description_edit.setText(self._initial_user_info.description)

        return main_widget

```

接下来，只需要实现`get_result()`方法即可大功告成。

**第三步：**实现`get_result()`方法，返回用户输入结果。

在本示例中，`get_result()`应当返回一个`UserInfo`对象。这将是非常简单的一件事，只需从对应的控件获取当前值，用这些值实例化`UserInfo`，然后返回该对象即可，具体代码如下：

```python
    def get_result(self) -> UserInfo:
        username = self._username_edit.text()
        birthday = self._birthday_edit.date().toPyDate()
        address = self._address_edit.text()
        email = self._email_edit.text()
        phone = self._phone_edit.text()
        description = self._description_edit.toPlainText()
        new_user_info = UserInfo(
            username=username,
            birthday=birthday,
            address=address,
            email=email,
            phone=phone,
            description=description,
        )
        return new_user_info
```

现在，我们的`UserInfoDialog`已经完成了，完整的代码如下：

```python
class UserInfoDialog(UniversalInputDialog):

    def __init__(
        self,
        parent: Optional[QWidget],
        title: str = "",
        icon: IconType = None,
        size: Tuple[int, int] = (400, 300),
        ok_button_text: str = "Ok",
        cancel_button_text: Optional[str] = "Cancel",
        initial_user_info: Optional[UserInfo] = None,
        **kwargs
    ):
        self._description_edit: Optional[QTextEdit] = None
        self._phone_edit: Optional[QLineEdit] = None
        self._email_edit: Optional[QLineEdit] = None
        self._address_edit: Optional[QLineEdit] = None
        self._birthday_edit: Optional[QDateEdit] = None
        self._username_edit: Optional[QLineEdit] = None
        self._initial_user_info: Optional[UserInfo] = initial_user_info
        super().__init__(
            parent,
            title=title,
            icon=icon,
            size=size,
            ok_button_text=ok_button_text,
            cancel_button_text=cancel_button_text,
            **kwargs
        )

    def get_result(self) -> UserInfo:
        username = self._username_edit.text()
        birthday = self._birthday_edit.date().toPyDate()
        address = self._address_edit.text()
        email = self._email_edit.text()
        phone = self._phone_edit.text()
        description = self._description_edit.toPlainText()
        new_user_info = UserInfo(
            username=username,
            birthday=birthday,
            address=address,
            email=email,
            phone=phone,
            description=description,
        )
        return new_user_info

    def create_main_widget(self) -> QWidget:
        ui_file = "user_info_dialog_main_widget.ui"
        # create widget from ui file
        main_widget = loadUi(ui_file)

        # obtain input widgets for UserInfo fields and set its initial values from initial_user_info
        self._username_edit = main_widget.findChild(QLineEdit, "username_edit")
        if self._initial_user_info:
            self._username_edit.setText(self._initial_user_info.username)

        self._birthday_edit = main_widget.findChild(QDateEdit, "birthday_edit")
        if self._initial_user_info:
            self._birthday_edit.setDate(self._initial_user_info.birthday)

        self._address_edit = main_widget.findChild(QLineEdit, "address_edit")
        if self._initial_user_info:
            self._address_edit.setText(self._initial_user_info.address)

        self._email_edit = main_widget.findChild(QLineEdit, "email_edit")
        if self._initial_user_info:
            self._email_edit.setText(self._initial_user_info.email)

        self._phone_edit = main_widget.findChild(QLineEdit, "phone_edit")
        if self._initial_user_info:
            self._phone_edit.setText(self._initial_user_info.phone)

        self._description_edit = main_widget.findChild(QTextEdit, "description_edit")
        if self._initial_user_info:
            self._description_edit.setText(self._initial_user_info.description)

        return main_widget
```

让我们写一个函数来测试一下它吧。

```python
def user_info_example(
    initial_username: str = "",
    initial_birthday: date = date(1990, 1, 1),
    initial_address: str = "",
    initial_email: str = "",
    initial_phone: str = "",
    initial_description: text_t = "",
):
    user_info = uinput.get_custom_input(
        UserInfoDialog,
        title="Get User Info",
        size=(350, 400),
        ok_button_text="Confirm",
        cancel_button_text="Dismiss",
        initial_user_info=UserInfo(
            username=initial_username,
            birthday=initial_birthday,
            address=initial_address,
            email=initial_email,
            phone=initial_phone,
            description=initial_description,
        ),
    )
    uprint(user_info)


if __name__ == "__main__":
    adapter = GUIAdapter()
    adapter.add(user_info_example)
    adapter.run()

```

效果如下：

<div style="text-align:center">
    <img src="/assets/custom_input_dialog_example.gif" />
</div>

最后，贴上完整代码：

> 可在[examples/]({{main_branch}}/examples/)目录下找到以下代码及相关的`.ui`文件。

```python
import dataclasses
from datetime import date
from typing import Optional, Tuple

from qtpy.QtWidgets import QWidget, QLineEdit, QTextEdit, QDateEdit
from qtpy.uic import loadUi

from pyguiadapter.adapter import uinput, GUIAdapter
from pyguiadapter.adapter.ucontext import uprint
from pyguiadapter.extend_types import text_t
from pyguiadapter.utils import IconType
from pyguiadapter.utils.inputdialog import UniversalInputDialog


@dataclasses.dataclass
class UserInfo:
    username: str
    birthday: date
    address: str
    email: str
    phone: str
    description: str


class UserInfoDialog(UniversalInputDialog):

    def __init__(
        self,
        parent: Optional[QWidget],
        title: str = "",
        icon: IconType = None,
        size: Tuple[int, int] = (400, 300),
        ok_button_text: str = "Ok",
        cancel_button_text: Optional[str] = "Cancel",
        initial_user_info: Optional[UserInfo] = None,
        **kwargs
    ):
        self._description_edit: Optional[QTextEdit] = None
        self._phone_edit: Optional[QLineEdit] = None
        self._email_edit: Optional[QLineEdit] = None
        self._address_edit: Optional[QLineEdit] = None
        self._birthday_edit: Optional[QDateEdit] = None
        self._username_edit: Optional[QLineEdit] = None
        self._initial_user_info: Optional[UserInfo] = initial_user_info
        super().__init__(
            parent,
            title=title,
            icon=icon,
            size=size,
            ok_button_text=ok_button_text,
            cancel_button_text=cancel_button_text,
            **kwargs
        )

    def get_result(self) -> UserInfo:
        username = self._username_edit.text()
        birthday = self._birthday_edit.date().toPyDate()
        address = self._address_edit.text()
        email = self._email_edit.text()
        phone = self._phone_edit.text()
        description = self._description_edit.toPlainText()
        new_user_info = UserInfo(
            username=username,
            birthday=birthday,
            address=address,
            email=email,
            phone=phone,
            description=description,
        )
        return new_user_info

    def create_main_widget(self) -> QWidget:
        ui_file = "user_info_dialog_main_widget.ui"
        # create widget from ui file
        main_widget = loadUi(ui_file)

        # obtain input widgets for UserInfo fields and set its initial values from initial_user_info
        self._username_edit = main_widget.findChild(QLineEdit, "username_edit")
        if self._initial_user_info:
            self._username_edit.setText(self._initial_user_info.username)

        self._birthday_edit = main_widget.findChild(QDateEdit, "birthday_edit")
        if self._initial_user_info:
            self._birthday_edit.setDate(self._initial_user_info.birthday)

        self._address_edit = main_widget.findChild(QLineEdit, "address_edit")
        if self._initial_user_info:
            self._address_edit.setText(self._initial_user_info.address)

        self._email_edit = main_widget.findChild(QLineEdit, "email_edit")
        if self._initial_user_info:
            self._email_edit.setText(self._initial_user_info.email)

        self._phone_edit = main_widget.findChild(QLineEdit, "phone_edit")
        if self._initial_user_info:
            self._phone_edit.setText(self._initial_user_info.phone)

        self._description_edit = main_widget.findChild(QTextEdit, "description_edit")
        if self._initial_user_info:
            self._description_edit.setText(self._initial_user_info.description)

        return main_widget


def user_info_example(
    initial_username: str = "",
    initial_birthday: date = date(1990, 1, 1),
    initial_address: str = "",
    initial_email: str = "",
    initial_phone: str = "",
    initial_description: text_t = "",
):
    user_info = uinput.get_custom_input(
        UserInfoDialog,
        title="Get User Info",
        size=(350, 400),
        ok_button_text="Confirm",
        cancel_button_text="Dismiss",
        initial_user_info=UserInfo(
            username=initial_username,
            birthday=initial_birthday,
            address=initial_address,
            email=initial_email,
            phone=initial_phone,
            description=initial_description,
        ),
    )
    uprint(user_info)


if __name__ == "__main__":
    adapter = GUIAdapter()
    adapter.add(user_info_example)
    adapter.run()
```

