from abc import abstractmethod
from typing import Any, List

NOT_APPLICABLE = -1


class CommonItemsViewInterface(object):

    @abstractmethod
    def row_count(self) -> int:
        pass

    def insert_row(self, row: int, row_data: Any):
        item = self.on_create_item(row, NOT_APPLICABLE)
        self.on_insert_item(row, NOT_APPLICABLE, item)
        self.on_set_item_data(row, NOT_APPLICABLE, row_data)

    def append_row(self, row_data: Any):
        self.insert_row(self.row_count(), row_data)

    def get_row_data(self, row: int) -> Any:
        return self.on_get_item_data(row, NOT_APPLICABLE)

    def get_all_row_data(self) -> List[Any]:
        return [self.get_row_data(row) for row in range(self.row_count())]

    def set_row_data(self, row: int, row_data: Any):
        return self.on_set_item_data(row, NOT_APPLICABLE, row_data)

    def remove_row(self, row: int) -> Any:
        self.on_remove_item(row, NOT_APPLICABLE)

    def remove_all_rows(self):
        for row in range(self.row_count() - 1, -1, -1):
            self.remove_row(row)

    def remove_rows(self, rows: List[int]):
        rows = set(rows)
        rows = sorted(rows, reverse=True)
        for row in rows:
            self.remove_row(row)

    def swap_rows(self, row1: int, row2: int):
        # this is the default implementation, which can be overridden by subclasses
        # this implementation swaps the data in the model and updates the view accordingly
        # it maybe not the most efficient way to swap rows, and may not completely work for all situations,
        # but it's simple enough and works in most cases.

        if row1 == row2:
            return

        # make sure row1 and row2 are valid
        row_count = self.row_count()
        if row_count <= row1 < 0 or row_count <= row2 < 0:
            raise IndexError("row out of range")

        # swap rows is to swap the data of the rows in the simple situation
        row_data1 = self.get_row_data(row1)
        row_data2 = self.get_row_data(row2)
        self.set_row_data(row1, row_data2)
        self.set_row_data(row2, row_data1)

    def get_selected_row(self, last_one: bool = False) -> int:
        if not self.get_selected_rows():
            return -1
        if last_one:
            return self.get_selected_rows()[-1]
        return self.get_selected_rows()[0]

    @abstractmethod
    def select_row(self, row: int):
        pass

    @abstractmethod
    def get_selected_rows(
        self,
        sort: bool = False,
        reverse: bool = False,
    ) -> List[int]:
        pass

    @abstractmethod
    def clear_selection(self):
        pass

    def move_row_up(self, row: int, steps: int = 1, wrap: bool = False) -> int:
        if steps < 0:
            raise ValueError("steps must be a positive integer")
        if steps == 0:
            return row  # no-op
        end_row = self._calc_movement(row, -steps, wrap)
        if end_row == row:
            return row  # no-op
        self.clear_selection()

        self.swap_rows(row, end_row)
        self.select_row(end_row)
        return end_row

    def move_row_down(self, row: int, steps: int = 1, wrap: bool = False):
        if steps < 0:
            raise ValueError("steps must be a positive integer")
        if steps == 0:
            return row  # no-op
        end_row = self._calc_movement(row, steps, wrap)
        if end_row == row:
            return row  # no-op
        self.clear_selection()
        self.swap_rows(row, end_row)
        self.select_row(end_row)
        return end_row

    @abstractmethod
    def on_create_item(self, row: int, col: int) -> Any:
        pass

    @abstractmethod
    def on_insert_item(self, row: int, col: int, item: Any):
        pass

    @abstractmethod
    def on_remove_item(self, row: int, col: int) -> Any:
        pass

    @abstractmethod
    def on_get_item_data(self, row: int, col: int) -> Any:
        pass

    @abstractmethod
    def on_set_item_data(self, row: int, col: int, value: Any):
        pass

    def _calc_movement(self, start_row: int, steps: int, wrap: bool):
        total = self.row_count()
        if not wrap:
            end_row = max(0, min(start_row + steps, total - 1))
        else:
            end_row = (start_row + steps) % total
        return end_row
