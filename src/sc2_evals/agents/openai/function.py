import json
from typing import Any, Callable, Optional

class FunctionSchema:
    def __init__(
        self,
        name: str,
        description: str,
        parameters: dict[str, Any],
        function: Callable,
        extra: Optional[dict[str, Any]]
    ):
        self.name = name
        self.description = description
        self.parameters = parameters
        self.function = function
        self.extra = extra

    async def __call__(self, arguments: str) -> Any:
        arguments_json = json.loads(arguments)
        if self.extra is None:
            output = await self.function(**arguments_json) 
        else:
            output = await self.function(**arguments_json, extra=self.extra)
        return output

    def to_dict(self) -> dict[str, Any]:
        function_dict: dict[str, Any] = {}
        function_dict["name"] = self.name
        function_dict["description"] = self.description
        function_dict["parameters"] = self.parameters
        return function_dict
