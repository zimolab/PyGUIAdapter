import dataclasses
from typing import List, Type, Optional, Any

from qtpy.QtWidgets import QWidget, QCommandLinkButton, QDialog


from ...common import CommonParameterWidget
from .editor import PathListEditor, PathListEditorConfig


@dataclasses.dataclass(frozen=True)
class PathListEditConfig(PathListEditorConfig):
    default_value: List[str] = dataclasses.field(default_factory=list)
    display_button_text: str = "Edit({} paths in total)"

    @classmethod
    def target_widget_class(cls) -> Type["PathListEdit"]:
        return PathListEdit


class PathListEdit(CommonParameterWidget):
    ConfigClass = PathListEditConfig

    def __init__(
        self,
        parent: Optional[QWidget],
        parameter_name: str,
        config: PathListEditConfig,
    ):
        self._value_widget: Optional[QCommandLinkButton] = None
        self._current_value: List[str] = []
        super().__init__(parent, parameter_name, config)

    def check_value_type(self, value: Any):
        if not isinstance(value, list):
            raise TypeError(f"Value must be a list, but got {type(value)}")

    @property
    def value_widget(self) -> QCommandLinkButton:
        if not self._value_widget:
            self._value_widget = QCommandLinkButton(self)
            self._value_widget.setText(
                self.config.display_button_text.format(len(self._current_value))
            )
            self._value_widget.clicked.connect(self._on_edit)
        return self._value_widget

    def set_value_to_widget(self, value: List[str]) -> None:
        self._current_value.clear()
        # self._current_value.extend(value)
        self._current_value = value
        self._update_value_widget()

    def get_value_from_widget(self) -> List[str]:
        return self._current_value

    def _on_edit(self):
        paths_editor = PathListEditor(self, self.config)
        paths_editor.path_list = self._current_value
        ret = paths_editor.exec_()
        if ret == QDialog.Accepted:
            self.set_value_to_widget(paths_editor.path_list)
        paths_editor.destroy()
        paths_editor.deleteLater()

    def _update_value_widget(self):
        display_text = self.config.display_button_text.format(len(self._current_value))
        self._value_widget.setText(display_text)


# if __name__ == "__main__":
#     app = QApplication([])
#     dialog = PathListEditor()
#     dialog.path_list = ["C:/Users/admin/Desktop/test1", "C:/Users/admin/Desktop/test2"]
#     dialog.show()
#     app.exec_()
#     print(dialog.path_list)
