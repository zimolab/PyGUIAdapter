class FunctionNotExecutingError(RuntimeError):
    pass


class NoSuchParameterError(RuntimeError):
    pass


class SetParameterValueError(RuntimeError):
    pass


class FunctionNotCancelableError(RuntimeError):
    pass


class NotCallableError(ValueError):
    pass
