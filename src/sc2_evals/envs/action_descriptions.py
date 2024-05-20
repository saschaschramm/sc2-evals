from typing import Callable

from pysc2.lib.actions import Function
from pysc2.lib import actions
from sc2_evals.agents.function_description import FunctionDescription
from sc2_evals.envs.action_description import ActionDescription


class ActionDescriptions:

    def __init__(self, screen_size: int):
        self._screen_size: int = screen_size

    def _available_action_names(self, available_actions: list[int]) -> list[str]:
        names: list[str] = []
        for action in available_actions:
            name = actions.FUNCTIONS[action].name
            names.append(name)
        return names

    def descriptions(self, action_fn: Callable) -> list[FunctionDescription]:
        action_descriptions = [
            ActionDescription.screen(minimum=0, maximum=self._screen_size - 1),
            ActionDescription.no_screen(),
        ]
        function_descriptions: list[FunctionDescription] = []
        for function_description in action_descriptions:
            function_descriptions.append(
                FunctionDescription(
                    name=function_description["name"],
                    description=function_description["description"],
                    parameters=function_description["parameters"],
                    function=action_fn,
                    extra=None,
                )
            )
        return function_descriptions

    def valid_actions(self, available_actions: list[int]) -> list[str]:
        available_names: list[str] = self._available_action_names(available_actions)
        description_names: list[str] = (
            ActionDescription.screen_names() + ActionDescription.no_screen_names()
        )
        return list(set(description_names) & set(available_names))


def print_action(name: str) -> None:
    action: Function = actions.FUNCTIONS[name]
    for arg in action.args:
        print(arg.name)
        print(arg.sizes)