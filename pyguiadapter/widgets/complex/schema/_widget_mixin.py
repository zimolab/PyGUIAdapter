from abc import abstractmethod
from typing import Any


class ValueWidgetMixin(object):
    @abstractmethod
    def set_value(self, value: Any):
        pass

    @abstractmethod
    def get_value(self) -> Any:
        pass
