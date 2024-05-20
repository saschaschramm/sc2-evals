from typing import Any, Optional

from openai.types.chat import (
    ChatCompletionSystemMessageParam,
    ChatCompletionUserMessageParam,
    ChatCompletionAssistantMessageParam,
    ChatCompletionMessageParam,
    ChatCompletionMessageToolCall,
    ChatCompletionMessageToolCallParam,
    ChatCompletionToolParam,
    ChatCompletionToolMessageParam,
)
from openai.types.chat.chat_completion_message_tool_call_param import Function
from openai.types.shared_params import FunctionDefinition


def _with_tool_call(
    tool_call: ChatCompletionMessageToolCall,
) -> ChatCompletionMessageToolCallParam:
    return ChatCompletionMessageToolCallParam(
        id=tool_call.id,
        function=Function(
            name=tool_call.function.name, arguments=tool_call.function.arguments
        ),
        type=tool_call.type,
    )

def assistant_message(
        content: Optional[str],
        tool_calls: Optional[list[ChatCompletionMessageToolCall]],
) -> ChatCompletionAssistantMessageParam:    
    if tool_calls is None:
        return ChatCompletionAssistantMessageParam(
            role="assistant",
            content=content)
    else:
        return ChatCompletionAssistantMessageParam(
            role="assistant",
            content=content,
            tool_calls=[_with_tool_call(tool_call) for tool_call in tool_calls])


def _tool(args: dict[str, Any]) -> ChatCompletionToolParam:
    # tool call
    return ChatCompletionToolParam(
                function=FunctionDefinition(**args), type="function"
            )

from sc2_evals.agents.function_description import FunctionDescription
def tools(functions: list[FunctionDescription]) -> list[ChatCompletionToolParam]:
    return [_tool(args=function.to_dict()) for function in functions]

def tool_message(content: str, tool_call_id: str) -> ChatCompletionToolMessageParam:
    # tool output
    return ChatCompletionToolMessageParam(content=content, role="tool", tool_call_id=tool_call_id)

def system_message(content: str) -> ChatCompletionSystemMessageParam:
    return ChatCompletionSystemMessageParam(content=content, role="system")

def user_message(content: str) -> ChatCompletionUserMessageParam:
    return ChatCompletionUserMessageParam(content=content, role="user")

def _with_message(message: dict[str, str]) -> ChatCompletionMessageParam:
    role: str = message["role"]
    if role == "user":
        return user_message(content=message["content"])
    elif role == "assistant":
        return assistant_message(
            content=message["content"],
            tool_calls=None,
        )
    elif role == "system":
        return system_message(content=message["content"])
    else:
        raise ValueError(f"Invalid role: {message['role']}")

def with_messages(messages: list[dict[str, str]]) -> list[ChatCompletionMessageParam]:
    return [_with_message(message) for message in messages]