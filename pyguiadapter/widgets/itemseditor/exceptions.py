class ValidationFailedError(ValueError):
    pass


class AlreadyExistError(ValueError):
    pass


class NotFoundError(ValueError):
    pass


class InsufficientColumnsError(ValueError):
    pass


class UnexpectedColumnError(ValueError):
    pass
