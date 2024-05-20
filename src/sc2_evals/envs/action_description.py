from typing import Any

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

class ActionDescription():

    @staticmethod
    def create_function_description(
        name, properties, description: str
    ) -> dict[str, Any]:
        return {
            "name": name,
            "description": description,
            "parameters": {
                "type": "object",
                "properties": properties
            },
        }
    
    @staticmethod
    def screen_names() -> list[str]:
            return [
                "Harvest_Gather_screen",
                "select_rect",
                "select_point",
                "Build_Refinery_screen",
                "Build_CommandCenter_screen",
                "Attack_screen",
            ]

    @staticmethod
    def no_screen_names() -> list[str]:
        return [
                "select_idle_worker",
                "Train_SCV_quick",
                "select_army",
                "Stop_quick",
                "HoldPosition_quick",
        ]

    
    @staticmethod
    def no_screen() -> dict[str, Any]:
        properties: dict[str, dict] = {}
        properties["name"] = _enum(
            ActionDescription.no_screen_names(), description="Action name"
        )
        function_description = ActionDescription.create_function_description(
            name="act",
            properties=properties,
            description=""
        )
        return function_description

    @staticmethod
    def screen(minimum: int, maximum: int) -> dict[str, Any]:
        properties: dict[str, dict] = {}
        properties["name"] = _enum(ActionDescription.screen_names(), description="Action name")
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
        function_description = ActionDescription.create_function_description(
            name="act_screen",
            properties=properties,
            description=""        
        )
        return function_description