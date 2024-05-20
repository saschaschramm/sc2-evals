from typing import Any

from openai import OpenAI
from openai.types.beta.function_tool_param import FunctionToolParam
from openai.types.beta import Assistant, Thread
from openai.types.shared_params import FunctionDefinition

from sc2_evals.agents.function_description import FunctionDescription
from sc2_evals.agents.models import Model, ModelInfo
from sc2_evals.agents.openai2.handler import EventHandler
from sc2_evals.agents.openai2.logger import Logger

class Agent():

    def __init__(self, model: Model, instructions: str, functions: list[FunctionDescription], logger: Logger):
        self._client: OpenAI = OpenAI()
        self._instructions: str = instructions
        self._functions: list[FunctionDescription] = functions
        self._thread: Thread = self._client.beta.threads.create()
        self._logger: Logger = logger
        self._logger.log_system_message(instructions=instructions, functions=functions)

        def _function_tools_params(functions: list[FunctionDescription]) -> list[FunctionToolParam]:
            function_tools_params: list[FunctionToolParam] = []
            for function in functions:
                function_tools_params.append(
                    FunctionToolParam(
                        function=FunctionDefinition(**function.to_dict()), type="function"
                    )
                )
            return function_tools_params

        function_descriptions: list[FunctionToolParam] = _function_tools_params(
            functions=self._functions
        )

        self.assistant: Assistant = self._client.beta.assistants.create(
            name="Starcraft",
            instructions=self._instructions, 
            tools=function_descriptions, 
            model=model.value,
            temperature=0.0
        )


    def run(self, message: dict[str, Any]):
        self._client.beta.threads.messages.create(
            thread_id=self._thread.id, 
            role=message["role"], 
            content=message["content"]
        )

        self._logger._step += 1
        self._logger.log_user_message(role=message["role"], content=message["content"])
        with self._client.beta.threads.runs.stream(
            thread_id=self._thread.id,
            assistant_id=self.assistant.id,
            instructions=self._instructions,
            #max_prompt_tokens=400,
            event_handler=EventHandler(self._client, self._functions, self._logger),
        ) as stream:
            stream.until_done()

    def delete(self):
        # TODO Delete in case of exception
        self._client.beta.assistants.delete(self.assistant.id)



