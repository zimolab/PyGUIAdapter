class ParameterError(Exception):
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


class FunctionExecutingError(RuntimeError):
    pass


class FunctionNotCancellableError(RuntimeError):
    pass


class FunctionNotExecutingError(RuntimeError):
    pass


class ParameterAlreadyExistError(RuntimeError):
    def __init__(self, parameter_name: str):
        self._parameter_name: str = parameter_name

    def message(self) -> str:
        return f"Parameter {self._parameter_name} already exists."

    @property
    def parameter_name(self) -> str:
        return self._parameter_name


class ParameterNotFoundError(RuntimeError):
    def __init__(self, parameter_name: str):
        self._parameter_name: str = parameter_name

    def message(self) -> str:
        return f"Parameter {self._parameter_name} not found."

    @property
    def parameter_name(self) -> str:
        return self._parameter_name


class ClipboardOperationError(RuntimeError):
    def __init__(self, operation: int, message: str):
        super().__init__(message)
        self._operation: int = operation

    @property
    def operation(self) -> int:
        return self._operation
