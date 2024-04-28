from typing import Union

from pysc2.lib.actions import FunctionCall, Function
from pysc2.lib import actions


def _string(description):
    return {"type": "string", "description": description}


def _integer(description, minimum, maximum):
    return {
        "type": "integer",
        "description": description,
        "minimum": minimum,
        "maximum": maximum,
    }


def _array(num_items, max, description):
    return {
        "type": "array",
        "minItems": num_items,
        "maxItems": num_items,
        "items": {
            "type": "integer",
            "minimum": 0,
            "maximum": max,
        },
        "description": description,
    }


def _tuple(num_items, max, description):
    return {
        "type": "array",
        "prefixItems": [{"type": "integer"}, {"type": "integer"}],
        "description": description,
    }


def _enum(enum_values, description):
    return {
        "type": "array",
        "items": {"type": "string", "enum": enum_values, "description": description},
    }


class Schema:

    @staticmethod
    def action_from_function_call(
        name: Union[str, list], x1=None, y1=None, x2=None, y2=None
    ) -> FunctionCall:
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
            return action(*arg_values)
        except:
            raise Exception(f"Invalid arguments for action {action}: {arg_values}")

    @staticmethod
    def _create_function_description(
        name, properties, description: str, required: list[str]
    ) -> dict:
        return {
            "name": name,
            "description": description,
            "parameters": {
                "type": "object",
                "properties": properties,
                "required": required,
            },
        }

    @staticmethod
    def screen_action_descriptions(minimum: int, maximum: int):
        properties: dict[str, dict] = {}
        properties["name"] = _enum(Schema.screen_actions(), description="Action name")
        # properties["name"] = _string(description="Action name")

        properties["x1"] = _integer(
            description="Screen position x", minimum=minimum, maximum=maximum
        )
        properties["y1"] = _integer(
            description="Screen position y", minimum=minimum, maximum=maximum
        )

        properties["x2"] = _integer(
            description="Screen position x", minimum=minimum, maximum=maximum
        )
        properties["y2"] = _integer(
            description="Screen position y", minimum=minimum, maximum=maximum
        )
        function_description = Schema._create_function_description(
            name="act_screen",
            properties=properties,
            description="Perform an action",
            required=["name", "x1", "y1"],
        )
        return function_description

    @staticmethod
    def no_screen_descriptions() -> dict:
        properties: dict[str, dict] = {}
        properties["name"] = _enum(
            Schema.no_screen_actions(), description="Action name"
        )
        # properties["name"] = _string(description="Action name")
        function_description = Schema._create_function_description(
            name="act",
            properties=properties,
            description="Perform an action",
            required=["name"],
        )
        return function_description

    @staticmethod
    def screen_actions() -> list[str]:
        return [
            "Harvest_Gather_screen",
            "select_rect",
            "select_point",
            "Build_Refinery_screen",
            "Build_CommandCenter_screen",
            "Attack_screen",
        ]

    @staticmethod
    def no_screen_actions():
        return [
            "select_idle_worker",
            "Train_SCV_quick",
            "select_army",
            "Stop_quick",
            "HoldPosition_quick",
        ]

    @staticmethod
    def descriptions(screen_size: int) -> list[dict]:
        descriptions: list[dict] = []
        descriptions.append(
            Schema.screen_action_descriptions(minimum=0, maximum=screen_size - 1)
        )
        descriptions.append(Schema.no_screen_descriptions())
        return descriptions

    @staticmethod
    def actions() -> list[str]:
        return Schema.screen_actions() + Schema.no_screen_actions()


def print_action(name: str) -> None:
    action: Function = actions.FUNCTIONS[name]
    for arg in action.args:
        print(arg.name)
        print(arg.sizes)


def print_descriptions() -> None:
    descriptions = Schema.descriptions(screen_size=32)
    import json

    print(json.dumps(descriptions, indent=4))


if __name__ == "__main__":
    print_descriptions()
    # print_action("HoldPosition_quick")
