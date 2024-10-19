from typing import Optional

from pyguiadapter.adapter import GUIAdapter
from pyguiadapter.exceptions import ParameterError
from pyguiadapter.windows.fnexec import FnExecuteWindowConfig


def equation_solver(a: float, b: float, c: float) -> Optional[tuple]:
    """
    Solving Equations: ax^2 + bx + c = 0 (a,b,c ∈ R, a ≠ 0)
    @param a: a ∈ R, a ≠ 0
    @param b: b ∈ R
    @param c: c ∈ R
    @return:
    """
    if a == 0:
        raise ParameterError(parameter_name="a", message="a cannot be zero!")

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
        output_dock_visible=False,
        clear_button_visible=False,
        clear_checkbox_visible=False,
        show_function_result=True,
        function_result_message="real roots: {}",
        default_parameter_group_name="Equation Parameters",
        print_function_error=False,
        print_function_result=False,
    )
    adapter = GUIAdapter()
    adapter.add(equation_solver, window_config=window_config)
    adapter.run()
