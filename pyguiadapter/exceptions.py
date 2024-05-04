class AlreadyExistsError(Exception):
    pass


class NotExistError(Exception):
    pass


class AppNotStartedError(Exception):
    pass


class ClassInitCancelled(Exception):
    pass


class MethodNotRegistered(Exception):
    pass
