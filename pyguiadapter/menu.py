import dataclasses
from typing import List, Union

from .action import Action, Separator


@dataclasses.dataclass(frozen=True)
class MenuConfig(object):
    title: str
    actions: List[Union[Action, Separator, "MenuConfig"]]
    separators_collapsible: bool = True
    tear_off_enabled: bool = True
    exclusive: bool = False

    def remove_action(self, action: Union[str, Action, Separator, "MenuConfig"]):
        if isinstance(action, str):
            for action_ in self.actions:
                if isinstance(action_, Action):
                    if action_.text == action:
                        action = action_
                        break
                if isinstance(action_, MenuConfig):
                    if action_.title == action:
                        action = action_
                        break
            if action in self.actions:
                self.actions.remove(action)
            return
        if action in self.actions:
            self.actions.remove(action)
            return
