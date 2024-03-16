from PyQt6.QtCore import QObject, pyqtSignal


class UPrint(QObject):
    printed = pyqtSignal(str, bool)

    def print(self, *args, sep=" ", end="\n", html: bool = False):
        # noinspection PyUnresolvedReferences
        self.printed.emit(sep.join([str(arg) for arg in args]) + end, html)


__uprint = UPrint()


def set_print_destination(func: callable):
    global __uprint
    # noinspection PyUnresolvedReferences
    __uprint.printed.connect(func)


def remove_print_destination(func: callable):
    global __uprint
    # noinspection PyUnresolvedReferences
    __uprint.printed.disconnect(func)


def uprint(*args, sep=" ", end="\n", html: bool = False):
    global __uprint
    __uprint.print(*args, sep=sep, end=end, html=html)
