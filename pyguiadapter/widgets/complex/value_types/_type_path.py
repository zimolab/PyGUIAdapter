class FilePathValue(ValueTypeBase):

    def __init__(self, default_value: str = ""):
        super().__init__(str(default_value))

    def validate(self, value: Any) -> bool:
        return isinstance(value, str)

    def hook_item_double_clicked(self) -> bool:
        return True

    def hook_item_clicked(self) -> bool:
        return False

    def create_item_editor_widget(
        self, parent: QWidget, *args, **kwargs
    ) -> Union[QWidget, ValueWidgetMixin]:
        return FilePathValueEdit(parent, self.default_value)

    def create_item_delegate_widget(self, parent: QWidget, *args, **kwargs) -> None:
        return None

    def on_item_double_clicked(
        self,
        source: QWidget,
        row: int,
        col: int,
        data: Any,
        item: QTableWidgetItem,
        *args,
        **kwargs,
    ):
        print(f"Double clicked: {data}")

    def on_item_clicked(
        self,
        source: QWidget,
        row: int,
        col: int,
        data: Any,
        item: QTableWidgetItem,
        *args,
        **kwargs,
    ):
        print(f"Clicked: {data}")
