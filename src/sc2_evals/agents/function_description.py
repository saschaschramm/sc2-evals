import json
from typing import Any, Callable, Optional

class FunctionDescription:
    def __init__(
        self,
        name: str,
        description: str,
        parameters: dict[str, Any],
        function: Callable,
        extra: Optional[dict[str, Any]]
    ):
        self._name = name
        self._description = description
        self._parameters = parameters
        self._function = function
        self._extra = extra

    def __call__(self, arguments: str) -> Any:
        arguments_json = json.loads(arguments)
        if self._extra is None:
            output = self._function(**arguments_json) 
        else:
            output = self._function(**arguments_json, extra=self._extra)
        return output

    def to_dict(self) -> dict[str, Any]:
        function_dict: dict[str, Any] = {}
        function_dict["name"] = self._name
        function_dict["description"] = self._description
        function_dict["parameters"] = self._parameters
        return function_dict
