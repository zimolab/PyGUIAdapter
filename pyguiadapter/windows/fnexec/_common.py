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
