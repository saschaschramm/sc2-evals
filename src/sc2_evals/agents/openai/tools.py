from openai.types.chat import ChatCompletionToolParam
from openai.types.shared_params import FunctionDefinition

from sc2_evals.agents.openai.function import FunctionSchema

def create_tool_params(functions: list[FunctionSchema]):
    tools: list[ChatCompletionToolParam] = []
    for function in functions:
        tools.append(
            ChatCompletionToolParam(
                function=FunctionDefinition(**function.to_dict()), type="function"
            )
        )
    return tools