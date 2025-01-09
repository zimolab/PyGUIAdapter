from typing import Any, Optional, Tuple

from qtpy.QtWidgets import QWidget

from ._variant import VariantEditor, VariantValue, VariantEditBox

WINDOW_TITLE = "Dict Editor"
WINDOW_SIZE = (600, 400)
CENTER_CONTAINER_TITLE = "Dict"
TEXT_FONT_SIZE = 14
TEXT_FONT_FAMILY = "Arial, Consolas, monospace"
FORMAT_BUTTON_TEXT = "Format"
VARIANT_EDITOR_BUTTON_TEXT = "Edit Dict"


class DictEditBox(VariantEditBox):
    def __init__(
        self,
        parent: QWidget,
        default_value: Any,
        *args,
        editor_button_text: str,
        window_title: str,
        window_size: Optional[Tuple[int, int]],
        center_container_title: str,
        text_font_size: int,
        text_font_family: str,
        format_button_text: Optional[str],
    ):
        super().__init__(
            parent,
            default_value,
            *args,
            editor_button_text=editor_button_text,
            window_title=window_title,
            window_size=window_size,
            center_container_title=center_container_title,
            text_font_size=text_font_size,
            text_font_family=text_font_family,
            format_button_text=format_button_text,
        )

    def on_create_variant_editor(self, **kwargs) -> "DictEditor":
        return DictEditor(self, self._value, **kwargs)


class DictEditor(VariantEditor):

    def __init__(
        self,
        parent: Optional[QWidget],
        default_value: dict,
        *,
        window_title: str,
        window_size: Optional[Tuple[int, int]],
        center_container_title: str,
        text_font_size: int,
        text_font_family: str,
        format_button_text: Optional[str],
    ):
        super().__init__(
            parent,
            default_value,
            window_title=window_title,
            window_size=window_size,
            center_container_title=center_container_title,
            text_font_size=text_font_size,
            text_font_family=text_font_family,
            format_button_text=format_button_text,
        )

    def from_variant_literal(self, variant_literal_str: str) -> Tuple[Any, bool]:
        value, ok = super().from_variant_literal(variant_literal_str)
        if not ok:
            return self._value, False
        if not isinstance(value, dict):
            self.show_error_message("Error", f"Not a valid dict!")
            return self._value, False
        return value, True

    def to_variant_literal(self, value: Any) -> Tuple[str, bool]:
        if not isinstance(value, dict):
            self.show_error_message("Error", f"Not a valid dict!")
            return repr(self._value), False
        literal_str, ok = super().to_variant_literal(value)
        if not ok:
            return repr(self._value), False
        return literal_str, True


class DictValue(VariantValue):
    def __init__(
        self,
        default_value: dict,
        *,
        display_name: Optional[str] = None,
        window_title: str = WINDOW_TITLE,
        window_size: Optional[Tuple[int, int]] = WINDOW_SIZE,
        center_container_title: str = CENTER_CONTAINER_TITLE,
        text_font_size: int = TEXT_FONT_SIZE,
        text_font_family: str = TEXT_FONT_FAMILY,
        format_button_text: Optional[str] = FORMAT_BUTTON_TEXT,
        editor_button_text: str = VARIANT_EDITOR_BUTTON_TEXT,
        readonly: bool = False,
        hidden: bool = False,
    ):
        super().__init__(
            default_value or {},
            display_name=display_name,
            window_title=window_title,
            window_size=window_size,
            center_container_title=center_container_title,
            text_font_size=text_font_size,
            text_font_family=text_font_family,
            format_button_text=format_button_text,
            editor_button_text=editor_button_text,
            readonly=readonly,
            hidden=hidden,
        )

    def validate(self, value: Any) -> bool:
        if value is None:
            return True
        if not isinstance(value, dict):
            return False
        return super().validate(value)

    def create_item_editor_widget(
        self, parent: QWidget, *args, **kwargs
    ) -> DictEditBox:
        return DictEditBox(
            parent,
            self.default_value,
            editor_button_text=self.editor_button_text,
            window_title=self.window_title,
            window_size=self.window_size,
            center_container_title=self.center_container_title,
            text_font_size=self.text_font_size,
            text_font_family=self.text_font_family,
            format_button_text=self.format_button_text,
        )

    def create_item_delegate_widget(
        self, parent: QWidget, *args, **kwargs
    ) -> DictEditor:
        return DictEditor(
            parent,
            self.default_value,
            window_title=self.window_title,
            window_size=self.window_size,
            center_container_title=self.center_container_title,
            text_font_size=self.text_font_size,
            text_font_family=self.text_font_family,
            format_button_text=self.format_button_text,
        )
