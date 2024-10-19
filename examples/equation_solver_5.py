from typing import Optional

from pyguiadapter.action import Action
from pyguiadapter.adapter import GUIAdapter
from pyguiadapter.adapter.uoutput import uprint
from pyguiadapter.exceptions import ParameterError
from pyguiadapter.menu import Menu
from pyguiadapter.utils import messagebox
from pyguiadapter.widgets import FloatSpinBoxConfig
from pyguiadapter.windows.fnexec import FnExecuteWindowConfig, FnExecuteWindow


def equation_solver_5(
    a: float = 1.0, b: float = 0.0, c: float = 0.0
) -> Optional[tuple]:
    """A simple equation solver for equations like:

    **ax^2 + bx + c = 0** (a, b, c ∈ **R** and a ≠ 0)

    @param a: a ∈ R and a ≠ 0
    @param b: b ∈ R
    @param c: c ∈ R
    @return:
    """
    if a == 0:
        raise ParameterError(parameter_name="a", message="a cannot be zero!")
    uprint(f"Equation:")
    uprint(f"  {a}x² + {b}x + {c} = 0")
    delta = b**2 - 4 * a * c
    if delta < 0:
        return None
    x1 = (-b + delta**0.5) / (2 * a)
    if delta == 0:
        return x1, x1
    x2 = (-b - delta**0.5) / (2 * a)
    return x1, x2


if __name__ == "__main__":
    window_config = FnExecuteWindowConfig(
        title="Equation Solver",
        icon="mdi6.function-variant",
        execute_button_text="Solve",
        size=(350, 450),
        document_dock_visible=False,
        show_function_result=True,
        function_result_message="roots: {}",
        default_parameter_group_name="Equation Parameters",
        # 隐藏`OutputDock`窗口
        output_dock_visible=False,
        # 因为隐藏了`OutputDock`窗口，所以无需将函数调用结果及函数异常信息打印到输出浏览器中
        print_function_error=False,
        print_function_result=False,
        # 隐藏清除按钮和清楚选框
        clear_button_visible=False,
        clear_checkbox_visible=False,
    )

    def on_action_about(wind: FnExecuteWindow, action: Action):
        messagebox.show_text_file(
            wind,
            text_file="./about.html",
            text_format="html",
            title="About",
        )

    action_about = Action(text="About", on_triggered=on_action_about)
    menu_help = Menu(title="Help", actions=[action_about])

    adapter = GUIAdapter()
    adapter.add(
        equation_solver_5,
        window_menus=[menu_help],
        window_config=window_config,
        widget_configs={
            "a": FloatSpinBoxConfig(
                default_value=1.0,
                decimals=5,
                step=0.00005,
            ),
            "b": FloatSpinBoxConfig(decimals=5, step=0.00005),
            "c": FloatSpinBoxConfig(decimals=5, step=0.00005),
        },
    )
    adapter.run()
