from typing import List

from .base import BaseCodeEditorWindow
from .constants import (
    DEFAULT_ICON_SIZE,
    ACTION_OPEN,
    ACTION_SAVE,
    ACTION_SAVE_AS,
    ACTION_QUIT,
    ACTION_UNDO,
    ACTION_REDO,
    ACTION_CUT,
    ACTION_COPY,
    ACTION_PASTE,
    ACTION_FORMAT_CODE,
    ACTION_SELECT_ALL,
    MENU_FILE,
    MENU_EDIT,
)
from ..action import Action, Separator
from ..menu import Menu
from ..toolbar import ToolBar


def _on_open_file(ctx: BaseCodeEditorWindow, _: Action):
    ctx.open_file()


def _on_save_file(ctx: BaseCodeEditorWindow, _: Action):
    ctx.save_file()


def _on_save_file_as(ctx: BaseCodeEditorWindow, _: Action):
    ctx.save_as_file()


def _on_quit(ctx: BaseCodeEditorWindow, _: Action):
    ctx.close()


def _on_undo(ctx: BaseCodeEditorWindow, _: Action):
    ctx.undo()


def _on_redo(ctx: BaseCodeEditorWindow, _: Action):
    ctx.redo()


def _on_cut(ctx: BaseCodeEditorWindow, _: Action):
    ctx.cut()


def _on_copy(ctx: BaseCodeEditorWindow, _: Action):
    ctx.copy()


def _on_paste(ctx: BaseCodeEditorWindow, _: Action):
    ctx.paste()


def _on_format_code(ctx: BaseCodeEditorWindow, _: Action):
    ctx.format_code()


def _on_select_all(ctx: BaseCodeEditorWindow, _: Action):
    ctx.select_all()


DEFAULT_ACTION_OPEN = Action(
    text=ACTION_OPEN,
    icon="fa.folder-open-o",
    shortcut="Ctrl+O",
    on_triggered=_on_open_file,
)

DEFAULT_ACTION_SAVE = Action(
    text=ACTION_SAVE,
    icon="fa.save",
    shortcut="Ctrl+S",
    on_triggered=_on_save_file,
)

DEFAULT_ACTION_SAVE_AS = Action(
    text=ACTION_SAVE_AS,
    icon="mdi.content-save-edit-outline",
    shortcut="Ctrl+Shift+S",
    on_triggered=_on_save_file_as,
)

DEFAULT_ACTION_QUIT = Action(
    text=ACTION_QUIT,
    icon="fa.window-close-o",
    shortcut="Ctrl+Q",
    on_triggered=_on_quit,
)

DEFAULT_ACTION_UNDO = Action(
    text=ACTION_UNDO,
    icon="fa.undo",
    shortcut="Ctrl+Z",
    on_triggered=_on_undo,
)

DEFAULT_ACTION_REDO = Action(
    text=ACTION_REDO,
    icon="fa.repeat",
    shortcut="Ctrl+Y",
    on_triggered=_on_redo,
)

DEFAULT_ACTION_CUT = Action(
    text=ACTION_CUT,
    icon="fa.cut",
    shortcut="Ctrl+X",
    on_triggered=_on_cut,
)

DEFAULT_ACTION_COPY = Action(
    text=ACTION_COPY,
    icon="fa.copy",
    shortcut="Ctrl+C",
    on_triggered=_on_copy,
)

DEFAULT_ACTION_PASTE = Action(
    text=ACTION_PASTE,
    icon="fa.paste",
    shortcut="Ctrl+V",
    on_triggered=_on_paste,
)

DEFAULT_ACTION_FORMAT_CODE = Action(
    text=ACTION_FORMAT_CODE,
    icon="fa.indent",
    shortcut="Ctrl+Alt+L",
    on_triggered=_on_format_code,
)


DEFAULT_ACTION_SELECT_ALL = Action(
    text=ACTION_SELECT_ALL,
    icon="fa.object-group",
    shortcut="Ctrl+A",
    on_triggered=_on_select_all,
)

DEFAULT_FILE_MENU = Menu(
    title=MENU_FILE,
    actions=[
        DEFAULT_ACTION_OPEN,
        DEFAULT_ACTION_SAVE,
        DEFAULT_ACTION_SAVE_AS,
        Separator(),
        DEFAULT_ACTION_QUIT,
    ],
)

DEFAULT_EDIT_MENU = Menu(
    title=MENU_EDIT,
    actions=[
        DEFAULT_ACTION_UNDO,
        DEFAULT_ACTION_REDO,
        Separator(),
        DEFAULT_ACTION_CUT,
        DEFAULT_ACTION_COPY,
        DEFAULT_ACTION_PASTE,
        Separator(),
        DEFAULT_ACTION_FORMAT_CODE,
        Separator(),
        DEFAULT_ACTION_SELECT_ALL,
    ],
)

DEFAULT_MENUS: List[Menu] = [DEFAULT_FILE_MENU, DEFAULT_EDIT_MENU]
DEFAULT_TOOLBAR = ToolBar(
    actions=[
        DEFAULT_ACTION_OPEN,
        DEFAULT_ACTION_SAVE,
        Separator(),
        DEFAULT_ACTION_UNDO,
        DEFAULT_ACTION_REDO,
        Separator(),
        DEFAULT_ACTION_CUT,
        DEFAULT_ACTION_COPY,
        DEFAULT_ACTION_PASTE,
        Separator(),
        DEFAULT_ACTION_FORMAT_CODE,
        Separator(),
        DEFAULT_ACTION_SELECT_ALL,
    ],
    moveable=True,
    icon_size=DEFAULT_ICON_SIZE,
)
