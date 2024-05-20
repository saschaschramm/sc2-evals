# json to FunctionCall
from typing import Union

from pysc2.lib.actions import FunctionCall, Function
from pysc2.lib import actions


class Action():

    def __init__(self, name: Union[str, list], x1=None, y1=None, x2=None, y2=None) -> None:
        # {'name': 'act_screen', 'arguments': '{"name": ["Attack_screen"], "x1": 10, "y1": 11}'}
        # {'name': 'act', 'arguments': '{"name":["select_army"]}'}
        try:
            if isinstance(name, list):
                action: Function = actions.FUNCTIONS[name[0]]
            elif isinstance(name, str):
                action: Function = actions.FUNCTIONS[name]
            else:
                raise Exception(f"Unknown action name type {name.__class__.__name__}")
        except:
            raise Exception(f"Unknown action {name}")

        arg_values = []
        for arg in action.args:
            if arg.name == "queued":
                arg_values.append(0)
            elif arg.name == "select_worker":
                arg_values.append(0)
            elif arg.name == "screen":
                if x1 is None:
                    raise Exception("x1 is missing")
                if y1 is None:
                    raise Exception("y1 is missing")
                arg_values.append([x1, y1])
            elif arg.name == "screen2":
                arg_values.append([x2, y2])
            elif arg.name == "select_point_act":
                # 0 means select
                arg_values.append(0)
            elif arg.name == "select_add":
                # 0 means select
                arg_values.append(0)
            else:
                raise Exception(f"Unknown argument name {arg.name}")
        try:
            self._function_call = action(*arg_values)
        except:
            raise Exception(f"Invalid arguments for action {action}: {arg_values}")

    @property
    def function_call(self) -> FunctionCall:
        return self._function_call