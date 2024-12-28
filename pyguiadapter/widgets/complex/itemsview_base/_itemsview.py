from abc import abstractmethod
from typing import Any, List


class ItemsViewInterface(object):

    @abstractmethod
    def insert_row(self, row: int, row_data: Any, *args, **kwargs):
        pass

    @abstractmethod
    def append_row(self, row_data: Any, *args, **kwargs):
        pass

    @abstractmethod
    def get_row_data(self, row: int, *args, **kwargs) -> Any:
        pass

    @abstractmethod
    def get_all_row_data(self, *args, **kwargs) -> List[Any]:
        pass

    @abstractmethod
    def set_row_data(self, row: int, row_data: Any, *args, **kwargs):
        pass

    @abstractmethod
    def remove_row(self, row: int, *args, **kwargs):
        pass

    @abstractmethod
    def remove_all_rows(self, *args, **kwargs):
        pass

    def remove_rows(self, rows: List[int], *args, **kwargs):
        rows = set(rows)
        rows = sorted(rows, reverse=True)
        for row in rows:
            self.remove_row(row, *args, **kwargs)

    @abstractmethod
    def row_count(self, *args, **kwargs) -> int:
        pass

    def swap_rows(self, row1: int, row2: int):
        # this is the default implementation, which can be overridden by subclasses
        # this implementation swaps the data in the model and updates the view accordingly
        # it maybe not the most efficient way to swap rows, and may not completely work for all situations,
        # but it's simple enough and works in most cases.
        data1 = self.get_row_data(row1)
        data2 = self.get_row_data(row2)
        self.set_row_data(row1, data2)
        self.set_row_data(row2, data1)

    @abstractmethod
    def select_row(self, row: int, *args, **kwargs):
        pass

    def get_selected_row(self, last_one: bool = False) -> int:
        if not self.get_selected_rows():
            return -1
        if last_one:
            return self.get_selected_rows()[-1]
        return self.get_selected_rows()[0]

    @abstractmethod
    def get_selected_rows(self, *args, **kwargs) -> List[int]:
        pass

    @abstractmethod
    def clear_selection(self, *args, **kwargs):
        pass

    def move_row_up(
        self, row: int, steps: int = 1, wrap: bool = False, *args, **kwargs
    ) -> int:
        if steps < 0:
            raise ValueError("steps must be a positive integer")
        if steps == 0:
            return row  # no-op
        end_row = self._calc_movement(row, -steps, wrap)
        if end_row == row:
            return row  # no-op
        self.clear_selection(*args, **kwargs)

        self.swap_rows(row, end_row)
        self.select_row(end_row, *args, **kwargs)
        return end_row

    def move_row_down(
        self, row: int, steps: int = 1, wrap: bool = False, *args, **kwargs
    ):
        if steps < 0:
            raise ValueError("steps must be a positive integer")
        if steps == 0:
            return row  # no-op
        end_row = self._calc_movement(row, steps, wrap)
        if end_row == row:
            return row  # no-op
        self.clear_selection(*args, **kwargs)
        self.swap_rows(row, end_row)
        self.select_row(end_row, *args, **kwargs)
        return end_row

    def _calc_movement(self, start_row: int, steps: int, wrap: bool):
        total = self.row_count()
        if not wrap:
            end_row = max(0, min(start_row + steps, total - 1))
        else:
            end_row = (start_row + steps) % total
        return end_row
