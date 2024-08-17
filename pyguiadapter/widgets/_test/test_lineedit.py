from pyguiadapter.widgets._test.ctx import TestContext
from pyguiadapter.widgets.edit.lineedit import LineEdit, LineEditConfig

if __name__ == "__main__":
    with TestContext() as ctx:
        # create parameter widgets
        args = LineEditConfig(
            default_value=None,
            description="param1 description",
        )
        lineedit_1 = LineEdit(None, "arg1", args).build()
        lineedit_1.label = "参数1"
        lineedit_1.description = "参数1描述"
        lineedit_1.default_value_description = "使用参数1默认值：{}"
        lineedit_1.set_value("1234")
        ctx.add_widget(lineedit_1)

        # start the qt application
        ctx.exec()
