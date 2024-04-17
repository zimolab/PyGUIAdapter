from PyQt6.QtCore import QObject, pyqtSignal


class UPrint(QObject):
    printed = pyqtSignal(str, bool)

    def print(self, *args, sep=" ", end="\n", html: bool = False):
        text = sep.join([str(arg) for arg in args]) + end
        # noinspection PyUnresolvedReferences
        self.printed.emit(text, html)


__uprint = UPrint()


def set_print_destination(func: callable):
    # noinspection PyUnresolvedReferences
    __uprint.printed.connect(func)


def remove_print_destination(func: callable):
    # noinspection PyUnresolvedReferences
    __uprint.printed.disconnect(func)


def uprint(*args, sep=" ", end="\n", html: bool = False):
    __uprint.print(*args, sep=sep, end=end, html=html)
