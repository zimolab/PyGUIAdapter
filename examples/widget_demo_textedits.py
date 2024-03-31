from pyguiadapter.adapter import GUIAdapter
from pyguiadapter.interact.uprint import uprint


def text_edits_demo(plain_text: str, sourcecode_text: str):
    """
    This demo shows text edits

    :param plain_text: show a plain text edit
    :param sourcecode_text: show a source code edit
    :return:

    @widgets
    [plain_text]
    widget_class="PlainTextEdit"

    [sourcecode_text]
    widget_class="CodeEdit"
    configs.AutoIndent=true
    configs.IndentationWidth=2
    configs.Lexer="JSON"
    configs.Folding="BoxTree"
    configs.EolMode="Unix"
    configs.WrapMode="WrapWord"
    configs.AutoCompletionSource="Document"
    configs.AutoCompletionCaseSensitivity=true
    configs.Font="Consolas"
    configs._FontSize=16
    @end
    """
    uprint("plain_text:", plain_text)
    uprint("sourcecode_text:", sourcecode_text)


if __name__ == "__main__":
    gui_adapter = GUIAdapter()
    gui_adapter.add(text_edits_demo)
    gui_adapter.run()
