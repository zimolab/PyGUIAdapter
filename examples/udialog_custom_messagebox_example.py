from datetime import date, datetime
from typing import Any
from uuid import uuid1

from qtpy.QtWidgets import QWidget, QVBoxLayout, QLabel, QDialogButtonBox

from pyguiadapter.adapter import GUIAdapter, BaseCustomDialog
from pyguiadapter.adapter import udialog
from pyguiadapter.adapter.uoutput import uprint
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
