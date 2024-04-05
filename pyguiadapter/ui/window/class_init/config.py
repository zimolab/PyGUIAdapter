import dataclasses
from typing import Optional

from pyguiadapter.ui.config import WindowConfig


@dataclasses.dataclass
class ClassInitWindowConfig(WindowConfig):
    title_label_text: Optional[str] = None
    init_button_text: Optional[str] = None
