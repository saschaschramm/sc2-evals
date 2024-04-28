import enum
from typing import Any, AsyncGenerator, Optional, Union

from openai import AsyncOpenAI
from openai._types import NOT_GIVEN
from openai.types.chat import (
    ChatCompletion,
    ChatCompletionToolParam,
    ChatCompletionMessage,
    ChatCompletionMessageParam,
    ChatCompletionMessageToolCall,
    ChatCompletionMessageToolCallParam,
    ChatCompletionAssistantMessageParam,
    ChatCompletionToolMessageParam,
    
)
from openai.types.chat.chat_completion_message_tool_call_param import Function
from openai.types.completion_usage import CompletionUsage

from sc2_evals.agents.openai.function import FunctionSchema
from sc2_evals.agents.openai.tools import create_tool_params

class FinishReason(enum.Enum):
    LENGTH = "length"
    STOP = "stop"
    TOOL_CALLS = "tool_calls"

class Response():
    def __init__(self, message: Union[ChatCompletionMessageParam, ChatCompletionMessageToolCallParam]):
        self.message = message

class ToolOutputResponse(Response):
    def __init__(self, message: ChatCompletionToolMessageParam, success: bool, metadata: Optional[dict[str, Any]]):
        # Example: {'content': '50.0', 'role': 'tool', 'tool_call_id': '<id>'}
        super().__init__(message)
        self.success = success
        self.metadata = metadata

class ToolCallResponse(Response):
    def __init__(self, message: ChatCompletionMessageToolCallParam, tool_name: str, arguments: str, tool_found: bool, completion_usage: Optional[CompletionUsage]):
        # Example {'id': '<id>', 'function': {'name': 'calculate', 'arguments': '{"expression":"13+37"}'}, 'type': 'function'}
        super().__init__(message)
        self.tool_name = tool_name
        self.arguments = arguments
        self.tool_found = tool_found
        self.completion_usage = completion_usage
        
class MessageResponse(Response):
    def __init__(self, message: ChatCompletionMessageParam, completion_usage: Optional[CompletionUsage], finish_reason: FinishReason):
        super().__init__(message)
        self.completion_usage = completion_usage
        self.finish_reason = finish_reason


class Agent:
    def __init__(
        self,
        client: AsyncOpenAI,
        model: str,
        max_completion_tokens: int,
        memory: bool,
        system_message: dict[str, str]
    ):
        self._model = model
        self._client = client
        self._max_completion_tokens = max_completion_tokens
        self._memory = memory
        self._system_message = system_message

    async def _chat_completion(
        self, functions: list[ChatCompletionToolParam], messages: list[ChatCompletionMessageParam]
    ) -> ChatCompletion:

        if len(functions) > 0:
            tools = functions
        else:
            tools = NOT_GIVEN

        # gpt-4-turbo-2024-04-09: max_context_length = 128000 tokens, max_completion_tokens = 4096 tokens
        # gpt-4-0125-preview: max_context_length = 128000 tokens, max_completion_tokens = 4096 tokens
        # gpt-4-1106-preview: max_context_length = 128000 tokens, max_completion_tokens = 4096 tokens
        # gpt-3.5-turbo-1106: max_context_length = 16385 tokens, max_completion_tokens = 4096 tokens
        chat_completion: ChatCompletion = await self._client.chat.completions.create(
            model=self._model,
            tools=tools,
            temperature=0,
            messages=messages,
            max_tokens=self._max_completion_tokens,
            seed=1337,
        )
        return chat_completion

    async def _find_function(self, name: str, functions: list[FunctionSchema]) -> FunctionSchema:
        selected_functions: list[FunctionSchema] = [
            function for function in functions if function.name == name
        ]
        if len(selected_functions) == 0:
            raise NotImplementedError(f"Unknown tool {name}")
        return selected_functions[0]

    def _finish_reason(self, chat_completion: ChatCompletion) -> FinishReason:
        try:
            return FinishReason(chat_completion.choices[0].finish_reason)
        except Exception:
            raise NotImplementedError(
                f"Unknown finish reason {chat_completion.choices[0].finish_reason}"
            )

    def _message(self, chat_completion: ChatCompletion) -> ChatCompletionMessage:
        assert len(chat_completion.choices) == 1
        return chat_completion.choices[0].message

    def _tokens(self, chat_completion: ChatCompletion) -> int:
        assert chat_completion.usage is not None
        return chat_completion.usage.total_tokens

    def _to_typed_dict(self, tool_calls):
        tool_calls_params: list[ChatCompletionMessageToolCallParam] = []
        for tool_call in tool_calls:
            tool_call_param = ChatCompletionMessageToolCallParam(id=tool_call.id,
                                                                 function=Function(name=tool_call.function.name, 
                                                                                   arguments=tool_call.function.arguments), 
                                                                                   type=tool_call.type)
            tool_calls_params.append(tool_call_param)
        return tool_calls_params

    async def run(self, messages: list[ChatCompletionMessageParam], functions: list[FunctionSchema]) -> AsyncGenerator[Response, None]:
        intermediate_messages: list[ChatCompletionMessageParam] = messages
        finish_reason: Optional[FinishReason] = None
        tools: list[ChatCompletionToolParam] = create_tool_params(functions)

        while finish_reason != FinishReason.STOP:
            # 1. messages = [user]
            # 2. messages = [user, tool_calls], intermediate_messages = [tool_calls]
            # 3. messages = [user, tool_calls, tool_outputs], intermediate_messages = [tool_calls, tool_outputs]
            # intermediate messages has to contain tool_call and tool_output
            chat_completion: ChatCompletion = await self._chat_completion(
                functions=tools, 
                messages=[self._system_message] + intermediate_messages
            )

            if self._memory is False:
                intermediate_messages = []

            completion_usage: Optional[CompletionUsage] = chat_completion.usage
            assert len(chat_completion.choices) == 1
            finish_reason = self._finish_reason(chat_completion)
            completion_message: ChatCompletionMessage = self._message(chat_completion)
            if finish_reason == FinishReason.LENGTH:
                # Don't try to parse tool because arguments are incomplete
                message = ChatCompletionAssistantMessageParam(
                        role=completion_message.role,
                        content=completion_message.content
                )
                yield MessageResponse(message, completion_usage=completion_usage, finish_reason=finish_reason)
                break

            elif finish_reason == FinishReason.TOOL_CALLS:
                # tool calls generated by the model
                tool_calls: Optional[
                    list[ChatCompletionMessageToolCall]
                ] = completion_message.tool_calls
                tool_call_params: list[ChatCompletionMessageToolCallParam] = self._to_typed_dict(tool_calls)
                tool_calls_message = ChatCompletionAssistantMessageParam(
                        role=completion_message.role,
                        content=completion_message.content,
                        tool_calls=tool_call_params
                    )
                intermediate_messages.append(tool_calls_message)
                # parallel tool calls
                for tool_call_param in tool_call_params:
                    # assumption: there is always a name and arguments
                    tool_name: str = tool_call_param.get("function").get("name")
                    arguments: str = tool_call_param.get("function").get("arguments")
                    id: str = tool_call_param.get("id")
                    # step 1: generate tool call
                    try:
                        function: FunctionSchema = await self._find_function(tool_name, functions)
                        yield ToolCallResponse(tool_call_param, tool_name, arguments, 
                                               tool_found=True, 
                                               completion_usage=completion_usage)
                    except:
                        yield ToolCallResponse(tool_call_param, tool_name, arguments, 
                                               tool_found=False, 
                                               completion_usage=completion_usage)

                    # step 2: run tool and retun output -> can take a long time
                    try:
                        output: dict[str, Any] = await function(arguments)
                        tool_output: ChatCompletionToolMessageParam = ChatCompletionToolMessageParam(
                            content=output["content"], role="tool", tool_call_id=id
                        )
                        intermediate_messages.append(tool_output)
                        yield ToolOutputResponse(tool_output, True, metadata=output["metadata"])
                    except Exception as e:
                        # in case the tool doesn't exist or the arguments are invalid
                        print("error", e)
                        tool_output: ChatCompletionToolMessageParam = ChatCompletionToolMessageParam(
                            content=repr(e), role="tool", tool_call_id=id)
                        intermediate_messages.append(tool_output)                        
                        yield ToolOutputResponse(tool_output, False, metadata=None)
            
            elif finish_reason == FinishReason.STOP:
                message = ChatCompletionAssistantMessageParam(
                        role=completion_message.role,
                        content=completion_message.content
                    )
                intermediate_messages.append(message)
                yield MessageResponse(message, completion_usage=completion_usage, finish_reason=finish_reason)
            else:
                raise NotImplementedError(f"Unknown finish reason {finish_reason}")