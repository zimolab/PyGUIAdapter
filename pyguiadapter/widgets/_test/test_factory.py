from qtpy.QtWidgets import QApplication

from pyguiadapter.fn import ParameterInfo
from pyguiadapter.widgets import ParameterWidgetFactory, LineEditConfig

app = QApplication([])

param_info = ParameterInfo(
    typename="str",
    type_args=[],
    default_value=0,
    description="test",
)
config = LineEditConfig(default_value=param_info.default_value)

w = ParameterWidgetFactory.create_widget(None, param_info, config)
w.show()

app.exec_()
