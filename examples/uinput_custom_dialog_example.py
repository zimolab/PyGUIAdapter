import dataclasses
from datetime import date
from typing import Optional, Tuple

from qtpy.QtWidgets import QWidget, QLineEdit, QTextEdit, QDateEdit
from qtpy.uic import loadUi

from pyguiadapter.adapter import uinput, GUIAdapter
from pyguiadapter.adapter.uoutput import uprint
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
