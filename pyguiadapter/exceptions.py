from __future__ import annotations


class ParameterValidationError(Exception):
    def __init__(self, parameter_name: str, message: str):
        self._parameter_name: str = parameter_name
        self._message: str = message
        super().__init__(message)

    @property
    def parameter_name(self) -> str:
        return self._parameter_name

    @property
    def message(self) -> str:
        return self._message


class AlreadyRegisteredError(Exception):
    pass


class NotRegisteredError(Exception):
    pass


class FunctionAlreadyExecutingError(RuntimeError):
    pass


class FunctionNotExecutingError(RuntimeError):
    pass
